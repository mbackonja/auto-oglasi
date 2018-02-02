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
  .controller('NavbarController', ($scope, $location, $http, ActiveUserService) => {
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
  })
  .directive('navigate', ($location) => {
    return (scope, element, attrs) => {
      let path

      attrs.$observe('navigate', (val) => {
        path = val
      })

      element.bind('click', () => {
        scope.$apply(() => {
          $location.path(path)
        })
      })
    }
  })
  .directive('ngFileModel', ['$parse', ($parse) => {
    return {
      restrict: 'A',
      link: (scope, element, attrs) => {
        let model = $parse(attrs.ngFileModel)
        let isMultiple = attrs.multiple
        let modelSetter = model.assign

        element.bind('change', () => {
          let values = []

          Array.from(element[0].files).forEach((item) => {
            let value = {
              name: item.name,
              size: item.size,
              url: URL.createObjectURL(item),
              _file: item
            }

            values.push(value)
          })

          scope.$apply(() => {
            if (isMultiple) {
              modelSetter(scope, values)
            } else {
              modelSetter(scope, values[0])
            }
          })
        })
      }
    }
  }])
