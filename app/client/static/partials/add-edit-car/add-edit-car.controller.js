app.controller('AddEditCarController', ($scope, $http, $location, $routeParams) => {
  $scope.action = $routeParams.action

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

  $scope.uploadedImages = null

  if ($scope.action === 'edit') {
    $http.get(`/api/cars/${$routeParams.id}`).then((response) => {
      $scope.uploadedImages = response.data.images.map((image) => {
        return {
          id: image.id,
          url: `static/img/cars/${$routeParams.id}/${image.path}`
        }
      })

      $scope.data = {
        make: response.data.make_id.toString(),
        model: response.data.model_id.toString(),
        year: response.data.year,
        mileage: response.data.km,
        price: response.data.price,
        condition: response.data.status,
        displacement: response.data.ccm,
        fuel_type: response.data.fuel_type,
        kw: response.data.kw,
        hp: response.data.hp,
        description: response.data.description,
        address: response.data.address,
        city: response.data.city,
        phone: response.data.phone,
        images: null
      }
    })
  }

  $http.get('/api/makes-and-models').then((response) => {
    $scope.makes = response.data.makes
    $scope.models = response.data.models
  })

  $scope.addOrCreate = () => {
    let formData = new FormData()
    for (let key in $scope.data) {
      if (key === 'images' && $scope.data['images']) {
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

    if ($scope.action === 'edit') {
      return $http.put(`/api/cars/${$routeParams.id}`, formData, config).then((response) => {
        swal({ title: 'Success!', text: response.data.message, type: 'success' }, () => {
          $location.path('/my-cars')
          $scope.$apply()
        })
      }).catch((error) => {
        swal('Error!', error.data.message, 'error')
      })
    }

    $http.post('/api/cars', formData, config).then((response) => {
      swal({ title: 'Success!', text: response.data.message, type: 'success' }, () => {
        $location.path('/my-cars')
        $scope.$apply()
      })
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }

  $scope.deleteImage = (imageId) => {
    return $http.delete(`/api/cars/${$routeParams.id}/images/${imageId}`).then((response) => {
      swal({ title: 'Success!', text: response.data.message, type: 'success' })
      $scope.uploadedImages.splice($scope.uploadedImages.findIndex((image) => { return image.id == imageId }), 1)
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
})
