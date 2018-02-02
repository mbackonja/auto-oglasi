app.controller('AddCarController', ($scope, $http, $location) => {
  $scope.makes = []
  $scope.models = []
  $scope.step = 1

  $scope.data = {
    make: '',
    model: '',
    year: '',
    mileage: '',
    price: '',
    condition: '',
    displacement: '',
    fuel_type: '',
    kw: '',
    hp: '',
    description: '',
    address: '',
    city: '',
    phone: '',
    images: null
  }

  $http.get('/api/makes-and-models').then((response) => {
    $scope.makes = response.data.makes
    $scope.models = response.data.models
  })

  $scope.goToStep2 = () => {
    $scope.step = 2
  }

  $scope.create = () => {
    console.log($scope.data)
  }
})
