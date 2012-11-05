'use strict';

/* Services */

angular.module('noodle.services', ['ngResource']).
    factory('Post', function($resource){
        return $resource('/stream/', {}, {
            get: {method:'GET', params:{phoneId:'phones'}, isArray:true}
        });
    }).
    factory('SharedService', function($rootScope){
        var share = {};
        share.alert = "";
        share.tags = [];

        share.loadAlert = function(alert) {
            this.alert = alert;
            $rootScope.$broadcast('loadAlert');
        };

        share.setCurrentTags = function(tags) {
            this.tags = tags;
            $rootScope.$broadcast('setCurrentTags')
        };

        return share;
    });

//angular.module('noodle.sharedServices', []).
//    factory('SharedService', function($rootScope){
//        var share = {};
//        share.alert = "";
//
//        share.renderAlert = function(alert) {
//            this.alert = alert;
//            $rootScope.$broadcast('renderAlert');
//        };
//
//        share.broadcastItem = function() {
//            $rootScope.$broadcast('handleBroadcast');
//        };
//
//        return share;
//    });

