app.controller('MyProductsController', ($scope, $http) => {
  $scope.products = []

  $http.get('/api/my-products').then((response) => {
    $scope.products = response.data
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
        $http.delete(`/api/my-products/${id}`).then(() => {
          $scope.products.splice($scope.products.findIndex((product) => { return product.id === id }), 1)
          // $scope.$apply()
        }).catch((error) => {
          swal('Error!', error.data.message, 'error')
        })
      }
    })
  }
})
