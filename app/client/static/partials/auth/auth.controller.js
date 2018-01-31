app.controller('AuthController', ['$scope', '$http', '$location', 'ActiveUserService', ($scope, $http, $location, ActiveUserService) => {
  $scope.registerData = {
    name: '',
    surname: '',
    email: '',
    password: '',
    passwordAgain: ''
  }

  $scope.loginData = {
    email: '',
    password: ''
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

  $scope.login = () => {
    $http.post('/api/login', $scope.loginData).then((response) => {
      ActiveUserService.setActiveUser(response.data)
      $location.path('/')
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
}])
