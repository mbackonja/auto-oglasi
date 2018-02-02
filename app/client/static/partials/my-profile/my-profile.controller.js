app.controller('MyProfileController', ($scope, $http, ActiveUserService) => {
  let activeUser = ActiveUserService.getActiveUser()

  $scope.personalData = {
    name: activeUser.name,
    surname: activeUser.surname,
    currentPassword: ''
  }

  $scope.loginData = {
    email: activeUser.email,
    newPassword: '',
    newPasswordAgain: '',
    currentPassword: ''
  }

  $scope.changePersonalData = () => {
    $http.put('/api/users/personal', $scope.personalData).then((response) => {
      let updatedUser = Object.assign(activeUser, {
        name: $scope.personalData.name,
        surname: $scope.personalData.surname
      })

      ActiveUserService.setActiveUser(updatedUser)
      swal({ title: 'Success!', text: response.data.message, type: 'success' })
      $scope.personalData.currentPassword = ''
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }

  $scope.changeLoginData = () => {
    $http.put('/api/users/login', $scope.loginData).then((response) => {
      let updatedUser = Object.assign(activeUser, {
        email: $scope.loginData.email
      })

      ActiveUserService.setActiveUser(updatedUser)
      $scope.loginData.currentPassword = ''
      $scope.loginData.newPassword = ''
      $scope.loginData.newPasswordAgain = ''
      swal({ title: 'Success!', text: response.data.message, type: 'success' })
    }).catch((error) => {
      swal('Error!', error.data.message, 'error')
    })
  }
})
