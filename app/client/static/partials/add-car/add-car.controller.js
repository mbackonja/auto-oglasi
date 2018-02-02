app.controller('AddCarController', ($scope, $http, $location) => {
  $scope.makes = []
  $scope.models = []

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

  $scope.create = () => {
    let formData = new FormData()
    for (let key in $scope.data) {
      if (key === 'images') {
        $scope.data['images'].forEach((image) => {
          formData.append('images', image._file)
        })
      } else {
        formData.append(key, $scope.data[key])
      }
    }
    let config = {
      transformRequest: angular.identity,
      headers: {
        'Content-Type': undefined
      }
    }

    $http.post('/api/cars', formData, config).then((response) => {
      swal({ title: 'Success!', text: response.data.message, type: 'success' }, () => {
        $location.path('/')
        $scope.$apply()
      })
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
})
