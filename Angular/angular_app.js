angular.module('MyApp', ['angularUtils.directives.dirPagination','oitozero.ngSweetAlert'])
   .controller('MainController', ['$scope','$http','SweetAlert',function($scope,$http,SweetAlert) { 

      $scope.greeting = "Angular Scope Connected";
      SweetAlert.swal("Success!", "User details have been Stored! ", "success");
      console.log("Hello");

}]);
