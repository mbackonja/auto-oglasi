app.controller('ProductController', ($scope, $http, $routeParams) => {
  $scope.product = {}

  $http.get(`/api/products/${$routeParams.id}`).then((response) => {
    $scope.product = response.data
  })
})
