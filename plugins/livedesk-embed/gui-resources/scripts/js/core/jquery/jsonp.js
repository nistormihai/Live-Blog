define(['jquery'],function(jQuery){
// // jquery.jsonp 2.3.1 (c)2012 Julian Aubourg | MIT License
// https://github.com/jaubourg/jquery-jsonp
(function(a){function b(){}function c(a){A=[a]}function d(a,b,c,d){try{d=a&&a.apply(b.context||b,c)}catch(e){d=!1}return d}function e(a){return/\?/.test(a)?"&":"?"}function D(l){function Y(a){Q++||(R(),K&&(y[M]={s:[a]}),G&&(a=G.apply(l,[a])),d(D,l,[a,t]),d(F,l,[l,t]))}function Z(a){Q++||(R(),K&&a!=u&&(y[M]=a),d(E,l,[l,a]),d(F,l,[l,a]))}l=a.extend({},B,l);var D=l.success,E=l.error,F=l.complete,G=l.dataFilter,H=l.callbackParameter,I=l.callback,J=l.cache,K=l.pageCache,L=l.charset,M=l.url,N=l.data,O=l.timeout,P,Q=0,R=b,S,T,U,V,W,X;return w&&w(function(a){a.done(D).fail(E),D=a.resolve,E=a.reject}).promise(l),l.abort=function(){!(Q++)&&R()},d(l.beforeSend,l,[l])===!1||Q?l:(M=M||h,N=N?typeof N=="string"?N:a.param(N,l.traditional):h,M+=N?e(M)+N:h,H&&(M+=e(M)+encodeURIComponent(H)+"=?"),!J&&!K&&(M+=e(M)+"_"+(new Date).getTime()+"="),M=M.replace(/=\?(&|$)/,"="+I+"$1"),K&&(P=y[M])?P.s?Y(P.s[0]):Z(P):(v[I]=c,V=a(s)[0],V.id=k+z++,L&&(V[g]=L),C&&C.version()<11.6?(W=a(s)[0]).text="document.getElementById('"+V.id+"')."+n+"()":V[f]=f,p in V&&(V.htmlFor=V.id,V.event=m),V[o]=V[n]=V[p]=function(a){if(!V[q]||!/i/.test(V[q])){try{V[m]&&V[m]()}catch(b){}a=A,A=0,a?Y(a[0]):Z(i)}},V.src=M,R=function(a){X&&clearTimeout(X),V[p]=V[o]=V[n]=null,x[r](V),W&&x[r](W)},x[j](V,U=x.firstChild),W&&x[j](W,U),X=O>0&&setTimeout(function(){Z(u)},O)),l)}var f="async",g="charset",h="",i="error",j="insertBefore",k="_jqjsp",l="on",m=l+"click",n=l+i,o=l+"load",p=l+"readystatechange",q="readyState",r="removeChild",s="<script>",t="success",u="timeout",v=window,w=a.Deferred,x=a("head")[0]||document.documentElement,y={},z=0,A,B={callback:k,url:location.href},C=v.opera;D.setup=function(b){a.extend(B,b)},a.jsonp=D})(jQuery)
});