'use strict';

/* Controllers */

function AlertCtrl($scope, SharedService) {
    $scope.alert = "";

    $scope.$on('loadAlert', function() {
        $scope.alert = SharedService.alert;
    });
}


function ChannelListCtrl($scope, $http, SharedService) {
    $scope.sendAlert = function(alert) {
        SharedService.loadAlert(alert);
    };

    $scope.loadChannels = function() {
        $http({method: 'GET', url: 'api/channel/get/'}).
            success(function(data, status, headers, config) {
                $scope.sendAlert(data.alert);
                $scope.channels = data.channels;
            }).error(function(data, status, headers, config) {});
    };

    $scope.addChannel = function() {
        $http({method: 'POST', url: 'api/channel/add/'}).
            success(function(data, status, headers, config) {
                $scope.sendAlert(data.alert);
                $scope.channels = data.channels;
            });
    };

    $scope.removeChannel = function(channelId) {
        $http({method: 'POST', url: 'api/channel/remove/', data:$.param({channel: channelId})}).
            success(function(data, status, headers, config) {
                $scope.sendAlert(data.alert);
                $scope.channels = data.channels;
            });
    };
}


function ChannelCtrl($scope, $http, SharedService) {
    $scope.id = '';
    $scope.name = '';
    $scope.tag = '';
    $scope.tags = [];

    $scope.selectChannel = function($scope) {
        console.log($scope.tags);
        console.log($scope);
        SharedService.setCurrentTags($scope.tags);
    };
}


function TagCtrl($scope, $http, SharedService) {
    $scope.tag = "";

    $scope.addTag = function() {
        $scope.tagSet[$scope.tag] = true;
        $scope.tag = '';
    };

    $scope.removeTag = function(tag) {
        delete $scope.tagSet[tag];
    };

    $scope.tagChannel = function() {
        $http({method: 'POST', url: 'api/channel/tag/add/', data:$.param({channel: $scope.id, tag: $scope.tag})}).
            success(function(data, status, headers, config) {
                $scope.tags.length = 0;
                $scope.tags.push.apply($scope.tags, data.tags);
                $scope.tag = "";
                SharedService.setCurrentTags($scope.tags);
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };

    $scope.untagChannel = function(channelId, tagName) {
        console.log($scope.tag);
        $http({method: 'POST', url: 'api/channel/tag/remove/', data:$.param({channel: channelId, tag: tagName})}).
            success(function(data, status, headers, config) {
                $scope.tags.length = 0;
                $scope.tags.push.apply($scope.tags, data.tags);
                SharedService.setCurrentTags($scope.tags);
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };
}


function PostCtrl($scope, $http, SharedService) {
    $scope.posts = [];
    $scope.title = '快來擁抱西藏樸素的美麗吧';
    $scope.body = '西藏的神秘與宗教總讓人感到遙遠 我從沒想過自己能在學生時期就能踏進這地方 畢竟西藏要襯年輕去啊！ 感恩的是參加交流團讓我不用走馬看花，能深入這個深不見底的世界 我從來沒有試過在客棧post文 只是看其他人打的 但真的好想跟大家分享我的西藏之旅 有甚麼意見隨便留言啊！！';
    $scope.tagSet = {};

    var _minPostTime = function() {
        var posts = $scope.posts;
        if (!(posts instanceof Array) || posts.length < 1)
            return null;
        var min = posts[0].time;
        for (var i = 1; i < posts.length; i++) {
            if ((posts[i].time) < min)
                min = posts[i].time;
        }
        return min;
    };

    var _setToArray = function(set) {
        var a = [];
        for (var key in set) {
            a.push(key);
        }
        return a;
    };

    $scope.sendAlert = function(alert) {
        SharedService.loadAlert(alert);
    };

    $scope.$on('setCurrentTags', function() {
        $scope.posts = [];
        $scope.loadPosts();
    });

    $scope.setPosts = function (posts) {
        $scope.posts = posts;
    };

    $scope.loadPosts = function() {
        var tags = SharedService.tags;
        if (!(tags instanceof Array)) tags = [];
        $http({method: 'GET', url: 'api/post/get/', params: {t: tags.join('+'), d: _minPostTime()}}).
            success(function(data, status, headers, config) {
                $scope.posts.push.apply($scope.posts, data.posts);
                $scope.minPostTime = _minPostTime();
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };

    $scope.autotag = function($scope) {
        $http({method: 'POST', url: 'api/post/autotag/', data: $.param({title: $scope.title, body:$scope.body})}).
            success(function(data, status, headers, config) {
                for (var i = 0; i < data.tags.length; i++) {
                    $scope.tagSet[data.tags[i].name] = true;
                }
                console.log($scope);
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };

    $scope.createPost = function($scope) {
        var tags = _setToArray($scope.tagSet);
        $http({method: 'POST', url: 'api/post/create/',
            data: $.param({title: $scope.title, body:$scope.body, tags: tags, repost: $scope.repost})}).
            success(function(data, status, headers, config) {
                $scope.setPosts([]);
                $scope.loadPosts();
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };
}

//PostCtrl.$inject = ['$scope', 'Post', 'SharedService'];

function PostReplyCtrl($scope) {
    $scope.title = '';
    $scope.body = '就戶外活動所使用的GPS來說，Garmin的戶外手持機的評價一向很好，也是許多戶外活動玩家所愛用的導航設備。長期以來，小弟都是Garmin 戶外用手持機的愛用者，從早期的GPS 12、eTrex系列、GPSmap 60系列到Oregon 550t、Dakota 20都愛不釋手，還曾經帶著GPSmap 60CSxc騎機車環島，靠者Garmin GPS的指引完成了我20年前未完的夢想，也帶著它登山朔溪以及划獨木舟。這些耐候性強大的手持機陪著我上山下海，帶著我走過不少山間小徑，總有柳暗花明的感動';
    $scope.tagSet = {};
    $scope.repost = '';
}



function PushCtrl($scope, $http) {
    $scope.body = "";
    $scope.pushes = [];

    $scope.push = function() {
        console.log($scope.post.id);
        console.log($scope.body);
        $http({method: 'POST', url: 'api/post/push/', data: $.param({post: $scope.post.id, body:$scope.body})}).
            success(function(data, status, headers, config) {
                $scope.pushes = data.pushes;
                $scope.body = "";
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };
}


function LivetagCtrl($scope, $http) {
    $scope.livetags = [];
    $scope.name = "";
    $scope.isVote = false;

    $scope.vote = function(livetagID) {
        $http({method: 'GET', url: 'api/tag/vote/', params: {t: livetagID}}).
            success(function(data, status, headers, config) {
                $scope.sendAlert(data.alert);
                $scope.livetags = data.tags;
            });
    };

    $scope.unvote = function(livetagID) {
        $http({method: 'GET', url: 'api/tag/unvote/', params: {t: livetagID}}).
            success(function(data, status, headers, config) {
                $scope.sendAlert(data.alert);
                $scope.livetags = data.tags;
            });
    };

    $scope.tag = function(itemID) {
        $http({method: 'POST', url: 'api/post/tag/', data: $.param({item: $scope.post.id, tag:$scope.name})}).
            success(function(data, status, headers, config) {
                $scope.livetags = data.tags;
            }).error(function(data, status, headers, config) {
                $scope.sendAlert(data);
            });
    };
}
