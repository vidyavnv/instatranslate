angular.module('MyApp', ['angularUtils.directives.dirPagination','oitozero.ngSweetAlert'])
   .controller('MainController', ['$scope','$http','SweetAlert','$location','$sce',function($scope,$http,SweetAlert,$location,$sce) { 


    $scope.greeting = "Angular Scope Connected";
    $scope.show=true;
    $scope.selectedVideo="";
    $scope.videoPlayer=false;
    //SweetAlert.swal("Success!", "User details have been Stored! ", "success");
    console.log("Hello");
    var APIUrl="http://localhost:5000";
    //$scope.current_playing="https://instatranslatefile.blob.core.windows.net/resources/ThinkDifferent_Video.mp4";


	$scope.languages=["en-US","fr-FR","de-DE"];
	
	//Code to upload Video and send Details to user: POST
  	$scope.upload_video = function() {
      	console.log($scope.video);
        var fd = new FormData();
        fd.append('file', $scope.video.video_file);
        $http.post(APIUrl+'/uploadFile', fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(){
        })
        .error(function(){
        });  

     	SweetAlert.swal("Success!", "Video has been uploaded! ", "success");
  	}


    $scope.uploadFile = function(files) {
            $scope.file = new FormData();
            $scope.file.append("file", files[0]);
        };

    $scope.playvideo = function(video_name) {
            $scope.$parent.current_playing = video_name;
            $scope.$parent.videoPlayer=true;
            console.log( $scope.current_playing);
            $scope.current_playing= video_name;
            var parent_element= document.getElementById("video_element");
            parent_element.src=video_name;
            parent_element.load();
            parent_element.play();
      };


    $scope.submitGuideDetailsForm= function() {
     console.log($scope.file);
     var mydata=$scope.video;
     console.log(mydata);
     $http.post(APIUrl+'/uploadFile', $scope.file, {
           headers: {'Content-Type': undefined },
           transformRequest: angular.identity,
           data: JSON.stringify(mydata)
          }).success(function(results) 
           {   
              console.log('success load file')
           }).error(function(error) 
           {  
              console.log('error load file!!!!!')
              console.log(error);
           });
           SweetAlert.swal("Request Submitted!", "Video will be available shortly! ", "success");
       };


  	//Code to get all videos in DB: GET
    $scope.get_all_videos=function(){
        $http({
              method: 'GET',
              url: APIUrl+"/getVideos",
              headers: {
                  'Content-type': 'application/json;'
              }
        })
        .then(function(response) {
          	console.log(response.data);
              $scope.videos = response.data;
              console.log($scope.videos);
        }, 
        function(rejection) {
              console.log( "failure message: " + JSON.stringify({data: data}));
        });
    }

    //Function for send request for translating videos: POST
    $scope.translatevideo=function(selectedVideo){
          console.log($scope.selectedVideo);
          $scope.selectedVideo.video_id=$scope.selectedVideo.insight_id;
          var res = $http.post(APIUrl+'/gettranslationreq',JSON.stringify($scope.selectedVideo));
          res.success(function(data, status, headers, config) {
            $scope.message = data;
          });
          res.error(function(data, status, headers, config) {
            alert( "failure message: " + JSON.stringify({data: data}));
          });
          SweetAlert.swal("Success!", "Translation Request Submitted, video will be available soon! ", "success");
    }


    $scope.trustSrc = function(src) {
      return $sce.trustAsResourceUrl(src);
    }


	$scope.redirect = function(){
  		$location.url('/convertvideo.html');
	}		

    $scope.goToConvert = function(curr_video) {
      	console.log(curr_video);
      	$scope.$parent.selectedVideo=curr_video;
      	console.log($scope.selectedVideo);
    };

   	$scope.check = function() {
      	console.log("Hello"+$scope.current_playing);
    };

	$scope.toggle = function() {
      	console.log($scope.show);
      	$scope.$parent.show=!$scope.$parent.show;
      	console.log($scope.show);
	};

}]);
