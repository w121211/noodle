'use strict';

/* Controllers */


function MyCtrl1() {}
MyCtrl1.$inject = [];


function MyCtrl2() {
}
MyCtrl2.$inject = [];


function GeneralCtrl($scope) {
    $scope.usingTags = ['tag1', 'tag2'];
}

function PostCtrl($scope, $http, Phone) {
    $scope.phone = $http({
        url: "http://example.appspot.com/rest/app2",
        method: "POST",
        data: {"foo":"bar"}
    }).success(function(data, status, headers, config) {
            $scope.data = data;
        }).error(function(data, status, headers, config) {
            $scope.status = status;
        });
//    $scope.phone = Phone.get({phoneId: 1}, function(phone) {
//        $scope.mainImageUrl = phone.images[0];
//    });
//    $scope.post = Post.getPost();
}
PostCtrl.$inject = ['$scope'];

function PostListCtrl($scope) {

}