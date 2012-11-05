'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('noodle.services', []).
  value('version', '0.1');

//angular.module('noodle.services', ['ngResource']).
//    factory('Post', function($resource) {
//        return $resource('url', {}, {
//            getPost: {method:'GET', params:{}, isArray:true}
//        });
//    });

angular.module('noodleServices', ['ngResource']).
    factory('Phone', function($resource){
        return $resource('phones/:phoneId.json', {}, {
            query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
        });
    });