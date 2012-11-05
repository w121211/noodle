'use strict';

/* App Module */

angular.module('noodle', ['noodle.filters', 'noodle.services', 'noodle.directives']).
    config(['$routeProvider', function($routeProvider) {
//    $routeProvider.when('/post/get/', {controller: PostCtrl});
    $routeProvider.otherwise({redirectTo: '/'});
////      when('/stream', {templateUrl: 'site_media/static/app/partials/phone-list.html',   controller: PostCtrl}).
////      when('/phones/:phoneId', {templateUrl: 'site_media/static/app/partials/phone-detail.html', controller: PhoneDetailCtrl}).
////      otherwise({redirectTo: '/stream'});
}]);