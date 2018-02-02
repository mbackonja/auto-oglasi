app.controller('CarController', ($scope, $http, $routeParams) => {
  $scope.car = {}

  $http.get(`/api/cars/${$routeParams.id}`).then((response) => {
    $scope.car = response.data
  })
})
