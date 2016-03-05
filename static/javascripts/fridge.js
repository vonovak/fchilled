
var Form = React.createClass({

    _onClick: function(e){
        e.preventDefault;
        this.props.resetFridge();
        this.sendMessage(this.props.tag, this.props.action);
        console.log('No!');

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
        <div className="form">
          <a href={'#'}>Yes!</a> | <a href={'#'} onClick={this._onClick}>No</a>
        </div>
    );
  }
})

var Item = React.createClass({
  render: function() {
    var data = this.props.data;

    if (!data.tag) {
        data.tag = "beer";
        data.filename = "beer";
        return <p>Insert items!</p>;
    }
    return (
        <div className="product">
          {data.tag}
          <img style="transform: rotate(90deg);" src={'http://fchilled.eu-gb.mybluemix.net/static/images/upload/' + data.filename + '.jpg'} />
          <Form resetFridge={this.props.resetFridge} tag={data.tag} action={data.action} />
        </div>
    );
  }
})

var Fridge = React.createClass({
  getInitialState: function() {
    return {data: {tag:'', name:'', filename:'', action:''}};
  },

    resetFridge: function() {
        this.setState({data: {tag:'', name:'', filename:'', action:''}});
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
      this.setState({data: {tag: product.tag, name: product.name, filename: product.filename, action:product.action}})
    }, this);
  },

  render: function() {
    return (
      <div className="commentBox">
        <h1>Fridge:</h1>
        <Item data={this.state.data} resetFridge={this.resetFridge} />
      </div>
    );
  }
})

ReactDOM.render(
  <Fridge />,
  document.getElementById('content')
);