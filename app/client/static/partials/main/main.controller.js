app.controller('MainController', ($scope, $http) => {
  $scope.products = []

  $http.get('/api/products').then((response) => {
    $scope.products = response.data
  })
})
