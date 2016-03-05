/**
 * Created by vojta on 3/5/16.
 */
if ('serviceWorker' in navigator) {
    console.log('Service Worker is supported');
    navigator.serviceWorker.register('/static/javascripts/sw.js').then(function (reg) {
        console.log(':^)', reg);
        // TODO
    }).catch(function (err) {
        console.log(':^(', err);
    });
}