/**
 * web.rpc - Compatibility module for Odoo 20
 */

odoo.define('web.rpc', [], function (require) {
    "use strict";
    
    return {
        query: function (params) {
            var route = params.route;
            var routeParams = params.params || {};
            
            return new Promise(function (resolve, reject) {
                fetch(route, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        jsonrpc: '2.0',
                        method: 'call',
                        params: routeParams,
                        id: Math.random(),
                    }),
                })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.error) {
                        reject(data.error);
                    } else {
                        resolve(data.result);
                    }
                })
                .catch(reject);
            });
        },
    };
});