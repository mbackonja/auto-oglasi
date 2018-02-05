app.controller('MainController', ($scope, $http) => {
  $scope.cars = []
  $scope.makes = []
  $scope.models = []
  $scope.searchData = {
    make: '',
    model: '',
    priceFrom: '',
    priceTo: '',
    fuelType: '',
    sortBy: 'id-asc'
  }

  $http.get('/api/makes-and-models').then((response) => {
    $scope.makes = response.data.makes
    $scope.models = response.data.models
  })

  $scope.search = () => {
    $http.post('/api/cars/search', $scope.searchData).then((response) => {
      $scope.cars = response.data
    })
  }

  $scope.clearResults = () => {
    $scope.searchData = {
      make: '',
      model: '',
      priceFrom: '',
      priceTo: '',
      fuelType: '',
      sortBy: 'id-asc'
    }

    getAllCars()
  }

  function getAllCars () {
    $http.get('/api/cars').then((response) => {
      $scope.cars = response.data
    })
  }

  getAllCars()
})
