app.controller('AddCarController', ($scope, $http, $location) => {
  $scope.makes = []
  $scope.models = []

  $scope.data = {
    make: '1',
    model: '1',
    year: 2010,
    mileage: 100,
    price: 1230,
    condition: 'New',
    displacement: 1599,
    fuel_type: 'LPG',
    kw: 10,
    hp: 20,
    description: 'Bla bla',
    address: 'adresaaaa',
    city: 'graaad',
    phone: '0631234567',
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
