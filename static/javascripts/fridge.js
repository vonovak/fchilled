
var Form = React.createClass({
  render: function () {
    return (
        <div className="form">
          <a href="#">Yes!</a> | <a href="">No</a>
        </div>
    );
  }
})

var Item = React.createClass({
  render: function() {
    var data = this.props.data;

    if (!data.tag) {
      return <p>Insert items!</p>;
    }
    return (
        <div className="product">
          {data.tag}
          <img src={'http://fchilled.eu-gb.mybluemix.net/uploads/' + data.filename + '.jpg'} />
          <Form />
        </div>
    );
  }
})

var Fridge = React.createClass({
  getInitialState: function() {
    return {data: {tag:'', name:'', filename:''}};
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
      this.setState({data: {tag: product.tag, name: product.name, filename: product.filename}})
    }, this);
  },

  render: function() {
    return (
      <div className="commentBox">
        <h1>Fridge:</h1>
        <Item data={this.state.data} />
      </div>
    );
  }
})

ReactDOM.render(
  <Fridge />,
  document.getElementById('content')
);