let app = angular.module('app', ['ngRoute'], ($interpolateProvider) => {
  $interpolateProvider.startSymbol('[[')
  $interpolateProvider.endSymbol(']]')
})

app.factory('ActiveUserService', ($q) => {
  let activeUser = window.user

  return {
    setActiveUser: (user) => {
      activeUser = user
    },

    getActiveUser: () => {
      return activeUser
    },

    hasAccess: (userType) => {
      if (userType === 'guest') {
        if (!activeUser) {
          return true
        }

        return $q.reject('Not guest')
      }

      if (userType === 'member') {
        if (activeUser) {
          return true
        }

        return $q.reject('Not logged')
      }

      if (userType === 'admin') {
        if (activeUser && activeUser.is_admin) {
          return true
        }

        return $q.reject('Not administrator')
      }
    }
  }
})

app.controller('NavbarController', ['$scope', '$location', '$http', 'ActiveUserService', ($scope, $location, $http, ActiveUserService) => {
  $scope.isActive = (viewLocation) => {
    return viewLocation === $location.path()
  }

  $scope.getActiveUser = () => {
    return ActiveUserService.getActiveUser()
  }

  $scope.isLogged = () => {
    return !!$scope.getActiveUser()
  }

  $scope.logout = () => {
    $http.post('/api/logout').then((response) => {
      ActiveUserService.setActiveUser(null)
    })
  }
}])
