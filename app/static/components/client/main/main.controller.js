app.controller('MainController', ['$scope', ($scope) => {
  $scope.products = [
    {
      id: 1,
      mark: 'Lada',
      model: 'Kalina',
      year: 2007,
      price: 10000
    },
    {
      id: 2,
      mark: 'Lada',
      model: 'Kalina',
      year: 2007,
      price: 10000
    }
  ]

  $scope.testMessage = 'asd'
}])
