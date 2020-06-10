var app = utils.app();
var params = new URLSearchParams(window.location.search);
app.data.loading = 0;
app.data.app = params.get('app');
app.data.dbname = params.get('dbname');
app.data.tablename = params.get('tablename');
app.data.url = '/_dashboard/rest/{app}/{dbname}/{tablename}'.format(app.data);
app.data.filter = params.get('filter') || '';
app.data.order = params.get('order') || '';
app.start();
