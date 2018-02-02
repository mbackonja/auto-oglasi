app.directive('carcard', () => {
  return {
    templateUrl: 'client/static/partials/car-card/car-card.component.html',
    restrict: 'E',
    scope: {
      car: '='
    }
  }
})
