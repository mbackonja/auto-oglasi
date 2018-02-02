app.controller('AddCarController', ($scope, $http, $location) => {
  $scope.makes = []
  $scope.models = []

  $scope.data = {
    make: '',
    model: ''
  }

  $http.get('/api/makes-and-models').then((response) => {
    $scope.makes = response.data.makes
    $scope.models = response.data.models
  })
})
