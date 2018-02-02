app.controller('MainController', ($scope, $http) => {
  $scope.cars = []

  $http.get('/api/cars').then((response) => {
    $scope.cars = response.data
  })
})
