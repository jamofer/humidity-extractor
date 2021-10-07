import React, { useEffect, useState } from 'react';
import { makeStyles, createStyles } from '@material-ui/core/styles';
import Slider from '@material-ui/core/Slider';
import Tooltip from '@material-ui/core/Tooltip';


const HOST = "humidity-extractor.local"
const PORT = 21000

const useStyles = makeStyles((theme) =>
  createStyles({
    root: {
      height: theme.spacing(3),
    }
  }),
);

const BASE_URL = "api"

function getExtractorStatus() {
  return fetch(`${BASE_URL}/status`)
    .then(data => data.json())
}

const setExtractorSpeed = (speed) => {
  fetch(
    `${BASE_URL}/configure`,
    {
      method: 'POST', 
      'headers': { 'Content-Type': 'application/json'}, 
      body: JSON.stringify({velocity: speed})
    }
  ).then(data => {
    console.log(data)
  })
}

const translateSpeeds = {
  off: 'Apagado',
  quiet: 'Silencioso',
  very_slow: 'Muy lento',
  slow: 'Lento',
  normal: 'Normal',
  fast: 'Rápido',
  very_fast: 'Muy rápido',
  maximum: 'Máximo',
};

const marks = (maxValue) => {
  return [
    {
      value: 0,
      label: 'Apagado',
    },
    {
      value: maxValue,
      label: 'Máximo',
    }
  ];
} 



function ValueLabelComponent(props) {
  const { children, open, value } = props;

  return (
    <Tooltip open={open} enterTouchDelay={0} placement="top" title={<h3>{value}</h3>} arrow>
      {children}
    </Tooltip>
  );
}

export default function SpeedComponent() {
  const classes = useStyles();

  const [speeds, setSpeeds] = useState([]);
  const [currentSpeed, setCurrentSpeed] = useState("off");
  const [value, setValue] = useState(0);

  useEffect(() => {
    getExtractorStatus().then(extractorStatus => {
      setSpeeds(extractorStatus.available_speeds);
      setCurrentSpeed(extractorStatus.current.speed);
    })
  }, [])

  useEffect(() => {
    setValue(speeds.indexOf(currentSpeed))
    console.log(speeds.indexOf(currentSpeed))
  }, [currentSpeed, speeds])

  if (speeds.length > 0) {
    return (
        <div className={classes.root}>
          <Slider
            value={value}
            getAriaValueText={(value) => translateSpeeds[speeds[value]]}
            valueLabelFormat={(value) => translateSpeeds[speeds[value]]}
            step={1}
            min={0}
            max={speeds.length - 1}
            marks={marks(speeds.length - 1)}
            valueLabelDisplay="on"
            ValueLabelComponent={ValueLabelComponent}
            onChange={(_, value) => setValue(value)}
            onChangeCommitted={(_, value) => setExtractorSpeed(speeds[value])}
          />
        </div>
    );
  }

  return (<div></div>)
}
