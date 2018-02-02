app.directive('productcard', () => {
  return {
    templateUrl: 'client/static/partials/product-card/product-card.component.html',
    restrict: 'E',
    scope: {
      product: '='
    }
  }
})
