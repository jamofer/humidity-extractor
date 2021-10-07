import { Container, Typography } from '@material-ui/core';
import SpeedComponent from './SpeedComponent';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(2),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '90%', // Fix IE 11 issue.
    marginTop: theme.spacing(6),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));


function App() {
  const classes = useStyles();

  return (
    <div className="App">
      <Container component="main" maxWidth="md">
      <Typography component="h1" variant="h3">
        Velocidad del extractor
      </Typography>
        <div className={classes.paper}>
          <form className={classes.form} noValidate>
            <SpeedComponent />
          </form>
        </div>
      </Container>
    </div>
  );
}

export default App;
