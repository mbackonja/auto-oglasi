app.controller('MyCarsController', ($scope, $http) => {
  $scope.cars = []

  $http.get('/api/my-cars').then((response) => {
    $scope.cars = response.data
  })

  $scope.delete = (id) => {
    swal({
      title: 'Are you sure?',
      text: 'Are you sure you want to delete this car?',
      icon: 'warning',
      showCancelButton: true,
      buttons: true,
      dangerMode: true,
      confirmButtonColor: '#DD6B55',
      confirmButtonText: 'Yes',
      cancelButtonText: 'No'
    }, (willDelete) => {
      if (willDelete) {
        $http.delete(`/api/my-cars/${id}`).then(() => {
          $scope.cars.splice($scope.cars.findIndex((car) => { return car.id == id }), 1)
        }).catch((error) => {
          swal('Error!', error.data.message, 'error')
        })
      }
    })
  }
})
