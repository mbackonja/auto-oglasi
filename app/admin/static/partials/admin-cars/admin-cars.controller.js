app.directive('admincars', () => {
  return {
    templateUrl: 'admin/static/partials/admin-cars/admin-cars.component.html',
    restrict: 'E',
    scope: {
      car: '='
    }
  }
})

app.controller('AdminCarsController', ($scope, $http, $location, ActiveUserService) => {
  $scope.nesto = 'asd'
  $scope.cars = []

  $http.get('/admin/api/cars').then((response) => {
    $scope.cars = response.data
  })

  $scope.delete = (carId) => {
    $http.delete(`/admin/api/cars/${carId}`).then((response) => {
      $scope.cars.splice($scope.cars.findIndex((car) => { return car.id == id }), 1)
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
})
