'''
Created on Aug 23, 2012

@package: superdesk media archive
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Ioan v. Pocol

Implementation for the audio persistence API.
'''

from ..core.spec import IThumbnailManager
from ..meta.meta_data import MetaDataMapped
from ..meta.audio_data import AudioDataEntry
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.support.sqlalchemy.session import SessionSupport
from ally.support.sqlalchemy.util_service import handle
from os import remove
from os.path import exists, splitext, abspath
from ally.support.util_sys import pythonPath
from sqlalchemy.exc import SQLAlchemyError
from subprocess import Popen, PIPE, STDOUT
from superdesk.media_archive.core.impl.meta_service_base import \
    thumbnailFormatFor, metaTypeFor
from superdesk.media_archive.core.spec import IMetaDataHandler
from superdesk.media_archive.meta.audio_data import META_TYPE_KEY
import re
from os.path import join

# --------------------------------------------------------------------

@injected
@setup(IMetaDataHandler, 'audioDataHandler')
class AudioPersistanceAlchemy(SessionSupport, IMetaDataHandler):
    '''
    Provides the service that handles the audio persistence @see: IAudioPersistanceService.
    '''
    
    format_file_name = '%(id)s.%(file)s'; wire.config('format_file_name', doc='''
    The format for the audios file names in the media archive''')
    default_format_thumbnail = '%(size)s/audio.jpg'; wire.config('default_format_thumbnail', doc='''
    The format for the audio thumbnails in the media archive''')
    format_thumbnail = '%(size)s/%(id)s.%(name)s.jpg'; wire.config('format_thumbnail', doc='''
    The format for the audio thumbnails in the media archive''')
    audio_supported_files = '3gp, act, AIFF, ALAC, Au, flac, gsm, m4a, m4p, mp3, ogg, ram, raw, vox, wav, wma'; wire.config('audio_supported_files', doc='''
    The audio formats supported by media archive audio plugin''')
    ffmpeg_path = join('workspace', 'tools', 'ffmpeg', 'bin', 'ffmpeg.exe'); wire.config('ffmpeg_path', doc='''
    The path where the ffmpeg is found''')
    
    thumbnailManager = IThumbnailManager; wire.entity('thumbnailManager')
    # Provides the thumbnail referencer

    def __init__(self):
        assert isinstance(self.format_file_name, str), 'Invalid format file name %s' % self.format_file_name
        assert isinstance(self.default_format_thumbnail, str), 'Invalid format thumbnail %s' % self.default_format_thumbnail
        assert isinstance(self.format_thumbnail, str), 'Invalid format thumbnail %s' % self.format_thumbnail
        assert isinstance(self.audio_supported_files, str), 'Invalid supported files %s' % self.audio_supported_files
        assert isinstance(self.ffmpeg_path, str), 'Invalid ffmpeg path %s' % self.ffmpeg_path
        SessionSupport.__init__(self)

        self.audioSupportedFiles = set(re.split('[\\s]*\\,[\\s]*', self.audio_supported_files))

    def deploy(self):
        '''
        @see: IMetaDataHandler.deploy
        '''
        
        self._defaultThumbnailFormat = thumbnailFormatFor(self.session(), self.default_format_thumbnail)
        self.thumbnailManager.putThumbnail(self._defaultThumbnailFormat.id, abspath(join(pythonPath(), 'resources', 'audio.jpg')))
        
        self._thumbnailFormat = thumbnailFormatFor(self.session(), self.format_thumbnail)
        self._metaTypeId = metaTypeFor(self.session(), META_TYPE_KEY).Id

    def processByInfo(self, metaDataMapped, contentPath, contentType):
        '''
        @see: IMetaDataHandler.processByInfo
        '''
        if contentType is not None and contentType.find(META_TYPE_KEY) > 0:
            return self.process(metaDataMapped, contentPath)

        extension = splitext(metaDataMapped.Name)[1][1:]
        if extension in self.audioSupportedFiles: return self.process(metaDataMapped, contentPath)

        return False

    def process(self, metaDataMapped, contentPath):
        '''
        @see: IMetaDataHandler.process
        '''
        assert isinstance(metaDataMapped, MetaDataMapped), 'Invalid meta data mapped %s' % metaDataMapped

        p = Popen((self.ffmpeg_path, '-i', contentPath), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        if p.wait() != 0:
            pass
            #TODO: ffmpeg requires an out parameter; I don't provide and get an error
            # if an out parameter is provided, it generates the output file 
            # found a trick, maybe a metadata operation, for example to add the generated id to the file? 
            #return False

        audioDataEntry = AudioDataEntry()
        audioDataEntry.Id = metaDataMapped.Id
        while True:
            line = p.stdout.readline()
            if not line: break
            line = str(line, 'utf-8')

            if line.find(': Audio: ') != -1:
                try:
                    values = self.extractAudio(line)
                    audioDataEntry.AudioEncoding = values[0]
                    audioDataEntry.SampleRate = values[1]
                    audioDataEntry.Channels = values[2]
                    audioDataEntry.AudioBitrate = values[3]
                except: pass
            elif line.find('Duration: ') != -1:
                try: 
                    values = self.extractDuration(line)
                    audioDataEntry.Length = values[0]
                    audioDataEntry.AudioBitrate = values[1]
                except: pass
            elif line.find('Output #0') != -1:
                break

        path = self.format_file_name % {'id': metaDataMapped.Id, 'file': metaDataMapped.Name}
        path = ''.join((META_TYPE_KEY, '/', self.generateIdPath(metaDataMapped.Id), '/', path))

        metaDataMapped.content = path
        metaDataMapped.typeId = self._metaTypeId
        metaDataMapped.thumbnailFormatId = self._defaultThumbnailFormat.id
        metaDataMapped.IsAvailable = True

        try:
            self.session().add(audioDataEntry)
            self.session().flush((audioDataEntry,))
        except SQLAlchemyError as e:
            metaDataMapped.IsAvailable = False
            handle(e, AudioDataEntry)

        return True

    # ----------------------------------------------------------------

    def extractDuration(self, line):
        #Duration: 00:00:30.06, start: 0.000000, bitrate: 585 kb/s
        properties = line.split(',')
        
        length = properties[0].partition(':')[2]
        length = length.strip().split(':')
        length = int(length[0]) * 60 + int(length[1]) * 60 + int(float(length[2]))

        bitrate = properties[2]
        bitrate = bitrate.partition(':')[2]
        bitrate = bitrate.strip().partition(' ')
        if bitrate[2] == 'kb/s':
            bitrate = int(float(bitrate[0]))
        else:
            bitrate = None

        return (length, bitrate)


    def extractAudio(self, line):
        #Stream #0.1(eng): Audio: aac, 44100 Hz, stereo, s16, 61 kb/s
        properties = (line.rpartition(':')[2]).split(',')

        index = 0
        encoding = properties[index].strip()

        index += 1
        sampleRate = properties[index].strip().partition(' ')
        if sampleRate[2] == 'Hz':
            sampleRate = int(float(sampleRate[0]))
        else:
            sampleRate = None

        index += 1
        channels = properties[index].strip()

        index += 2
        bitrate = properties[4].strip().partition(' ')
        if bitrate[2] == 'kb/s':
            bitrate = int(float(bitrate[0]))
        else:
            bitrate = None

        return (encoding, sampleRate, channels, bitrate)

    # ----------------------------------------------------------------

    def generateIdPath (self, id):
        return "{0:03d}".format((id // 1000) % 1000)
