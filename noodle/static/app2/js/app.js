'use strict';


// Declare app2 level module which depends on filters, and services
angular.module('noodle', ['noodle.filters', 'noodleServices', 'noodle.directives']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'site_media/static/app2/partials/partial1.html', controller: MyCtrl1});
    $routeProvider.when('/view2', {templateUrl: 'site_media/static/app2/partials/partial2.html', controller: MyCtrl2});

    $routeProvider.when('/post', {templateUrl: 'site_media/static/app2/partials/post.html', controller: PostCtrl});
    $routeProvider.otherwise({redirectTo: '/post'});
  }]);
