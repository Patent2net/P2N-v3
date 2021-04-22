const e = React.createElement;

const LikeButton = function (){
    const [ liked, setLiked ] = React.useState(false);
  
    if (liked) {
        return 'You liked this.';
    }

    return e(
    'button',
    { onClick: () => setLiked(true) },
    'Like'
    );
}

const domContainer = document.querySelector('#request');
ReactDOM.render(e(LikeButton), domContainer);