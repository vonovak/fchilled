
var Form = React.createClass({

	_onClick: function(e){
		e.preventDefault;
		this.props.resetFridge(this.props.tag, this.props.action);
		this.sendMessage(this.props.tag, this.props.action);
		console.log('No!');

	},

    _onClickYes: function(e) {
        e.preventDefault;
        this.props.resetFridge('', '');
    },

	sendMessage: function(tag, action) {
		var message = {
			tag: tag,
			action: action
		}
		$.post('/revert', message).success(function() {
			console.log('posted');
		});
	},

  render: function () {
	return (
		<div className="form row">
		  <a href={'#'} className="btn btn-success btn-lg col-xs-6" onClick={this._onClickYes}>Yes!</a><a href={'#'} className="btn btn-lg btn-danger col-xs-6" onClick={this._onClick}>No</a>
		</div>
	);
  }
})

var Product = React.createClass({
	render: function() {
		return (
            <tr>
			    <th>{this.props.productName}</th>
                <td>{this.props.productCount}</td>
            </tr>
		);
	}
})

var Products = React.createClass({
	render: function() {
		return (
		<div className="products row">
            <div className="col-sm-6 col-sm-offset-3">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th className="alignLeft">Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <Product productName="Coca-Cola" productCount={this.props.counts.cocacola} />
                        <Product productName="Juice" productCount={this.props.counts.juice} />
                        <Product productName="Beer" productCount={this.props.counts.beer} />
                        <Product productName="Bottled Water" productCount={this.props.counts.waterbottle} />
                    </tbody>
                </table>
            </div>
		</div>
		);
	}
})

var Item = React.createClass({
  render: function() {
	var data = this.props.data;

	if (!data.tag) {
		return <p></p>;
	}
	return (
		<div className="product">
		  <h2 className="itemName"><span>{data.tag}</span></h2>
		  <img src={'http://fchilled.eu-gb.mybluemix.net/static/images/upload/' + data.filename + '.jpg'} />
		  <Form resetFridge={this.props.resetFridge} tag={data.tag} action={data.action} />
		</div>
	);
  }
})

var Fridge = React.createClass({
  getInitialState: function() {
	return {
		data: {tag:'', name:'', filename:'', action:''},
		counts: {beer: countData.beer, cocacola: countData.cocacola, waterbottle: countData.waterbottle, juice: countData.juice}
	};
  },

	resetFridge: function(tag, action) {
        this.state.data = {tag:'', name:'', filename:'', action:''}
        var diff = 1;
        if (action == 'add') {
            diff = -1;
        }
        if (tag == 'cocacola') {
            this.state.counts.cocacola += diff;
        } else if (tag == 'juice') {
            this.state.counts.juice += diff;
        } else if (tag == 'waterbottle') {
            this.state.counts.waterbottle += diff;
        } else if (tag == 'beer') {
            this.state.counts.beer += diff;
        }

		this.setState(this.state);
		console.log('Fridge reseted!');
	},

  componentWillMount: function() {
	this.pusher = new Pusher('99c8766f736643bbdfa2', {
	  cluster: 'eu',
	  encrypted: true
	});
	this.productShelf = this.pusher.subscribe('messages');
  },

  componentDidMount: function() {
	this.productShelf.bind('new_product', function(product){
	  this.setState({
          data: {tag: product.tag, name: product.name, filename: product.filename, action:product.action},
          counts: {beer: product.productMap.beer, cocacola: product.productMap.cocacola,
			  waterbottle: product.productMap.waterbottle, juice: product.productMap.juice}
      })
	}, this);
  },

  render: function() {
	return (
	  <div className="commentBox">
		<Item data={this.state.data} resetFridge={this.resetFridge} />
		<Products counts={this.state.counts} />
	  </div>
	);
  }
})

ReactDOM.render(
  <Fridge />,
  document.getElementById('content')
);