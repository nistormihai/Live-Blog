'''
Created on Mar 9, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

API specifications for PO file management.
'''

from ally.api.config import service, call
from introspection.api.plugin import Plugin
from introspection.api.component import Component
from ally.api.type import Reference
from ally.api.model import Content
from introspection.api import modelDevel

# --------------------------------------------------------------------

@modelDevel(id='Locale')
class PO:
    '''
    Model for a PO file.
    '''
    Locale = str
    Reference = Reference

# --------------------------------------------------------------------

@service
class IPOFileService:
    '''
    The PO file management service.
    '''

    @call
    def getGlobalPOFile(self, locale:PO.Locale) -> PO.Reference:
        '''
        Provides the messages for the whole application and the given locale.

        @param locale: string
            The locale for which to return the translation.
        @return: string
            The path to the temporary PO file.
        '''

    @call
    def getComponentPOFile(self, component:Component.Id, locale:PO.Locale) -> PO.Reference:
        '''
        Provides the messages for the given component and the given locale.

        @param locale: string
            The locale for which to return the translation.
        @param component: Component.Id
            The component for which to return the translation.
        @return: string
            The path to the temporary PO file.
        '''

    @call
    def getPluginPOFile(self, plugin:Plugin.Id, locale:PO.Locale) -> PO.Reference:
        '''
        Provides the messages for the given plugin and the given locale.

        @param locale: string
            The locale for which to return the translation.
        @param plugin: Plugin.Id
            The plugin for which to return the translation.
        @return: string
            The path to the temporary PO file.
        '''

    @call
    def updateGlobalPOFile(self, poFile:Content, locale:PO.Locale):
        '''
        Updates the messages for all components / plugins and the given locale.

        @param poFile: file like object
            The source PO file from which to read the translation.
        @param locale: string
            The locale for which to update the translation.
        '''

    @call
    def updateComponentPOFile(self, poFile:Content, component:Component.Id, locale:PO.Locale):
        '''
        Updates the messages for the given component and the given locale.

        @param poFile: file like object
            The source PO file from which to read the translation.
        @param locale: string
            The locale for which to update the translation.
        @param component: Component.Id
            The component for which to update the translation.
        '''

    @call
    def updatePluginPOFile(self, poFile:Content, plugin:Plugin.Id, locale:PO.Locale):
        '''
        Updates the messages for the given plugin and the given locale.

        @param poFile: file like object
            The source PO file from which to read the translation.
        @param locale: string
            The locale for which to update the translation.
        @param plugin: Plugin.Id
            The plugin for which to update the translation.
        '''