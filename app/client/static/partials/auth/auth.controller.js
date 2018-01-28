app.controller('AuthController', ['$scope', '$http', ($scope, $http) => {
  $scope.registerData = {
    name: '',
    surname: '',
    email: '',
    password: '',
    passwordAgain: ''
  }

  $scope.register = () => {
    $http.post('/api/register', $scope.registerData).then((response) => {
      swal('Success!', response.data.message, 'success')
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
}])
