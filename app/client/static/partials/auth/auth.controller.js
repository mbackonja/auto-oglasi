app.controller('AuthController', ['$scope', '$http', '$location', 'ActiveUserService', ($scope, $http, $location, ActiveUserService) => {
  $scope.registerData = {
    name: '',
    surname: '',
    email: '',
    password: '',
    passwordAgain: ''
  }

  $scope.register = () => {
    $http.post('/api/register', $scope.registerData).then((response) => {
      ActiveUserService.setActiveUser($scope.registerData)
      swal({ title: 'Success!', text: response.data.message, type: 'success' }, () => {
        $location.path('/')
        $scope.$apply()
      })
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
}])
