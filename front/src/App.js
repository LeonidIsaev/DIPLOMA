import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import { useState } from 'react';
import Graph from "react-vis-network-graph";
import { useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Tabs, Carousel } from 'antd';
import { Column } from '@antv/g2plot';
const contentStyle = {
  background: '#364d79',
};
function App() {
  const [graph,setGraph]=useState(null)
  const [graph_list,setGraphlist]=useState(null)
  const [inputNode,setInputNode] = useState('')
  const [inputEdge1,setinputEdge1] = useState('')
  const [inputEdge2,setinputEdge2] = useState('')
  const [nvalue,setnvalue] = useState('')
  const [kvalue,setkvalue] = useState('')
  const [canonic_code,setcanonic_code] = useState('')
  const [partial,setPartial] = useState('None')
  const [TimeStat,setTimeStat] = useState([])
  const { TabPane } = Tabs;

  const kek = ()=>{
    axios.get('http://localhost:5000').then(resp=>{setGraph(resp.data)})
  } 
  const kekAddNode = ()=>{
    axios.post('http://localhost:5000/addNode',{inputNode:inputNode}).then(resp=>{setGraph(resp.data)})
  } 
  const kekAddEdge = ()=>{
    axios.post('http://localhost:5000/addEdge',{inputEdge1:inputEdge1,inputEdge2:inputEdge2}).then(resp=>{setGraph(resp.data)})
  }
  const kekLoadlist = ()=>{
    axios.post('http://localhost:5000/list',{nvalue:nvalue,kvalue:kvalue,partial:partial}).then(resp=>{setGraphlist(resp.data)})
  }

  const kekLoadTimeStat = ()=>{
    axios.get('http://localhost:5000/get_time_stat').then(resp=>{setTimeStat(resp.data)})
  }

  const kekClear = ()=>{
    axios.get('http://localhost:5000/clear').then(resp=>{setGraph(resp.data)})
  }

  const kekgetCanonicalCode = ()=>{
    axios.get('http://localhost:5000/getCanonicalCode').then(resp=>{setcanonic_code(resp.data)})
  }

  useEffect(()=>{
    if (TimeStat.length > 0)
    { 
      let time_chart_div = document.getElementById('container_time')
      while (time_chart_div.hasChildNodes()){
        time_chart_div.removeChild(time_chart_div.lastChild)
      }
      const columnPlot = new Column('container_time', {
        data : TimeStat,
        xField: 'n',
        yField: 'time',
        },
      );
      columnPlot.render(); 
    }
  },[TimeStat])


  const options = {
    edges: {
      color: "#000000",
      arrows: {
        to: {
          enabled: false,
        }
      }
    },
    height: "800px",
    physics: false
  }
  const events = {
    select: function(event) {
      var { nodes, edges } = event;
    }
  }
  return (
    <div className="App">
      <div className="card-container">
        <Tabs tabPosition='left' type="card" onTabClick={key => {key==='3' && kekLoadTimeStat()}}>
          <TabPane tab="Построение дерева" key="1" >
            <div className='buttons-group'>
              <button onClick={kek}> get </button>
              <input type='text' value={inputNode} onChange={e=>setInputNode(e.target.value)} placeholder="Node"/>
              <button onClick={kekAddNode}> add node </button>
              <input type='text' value={inputEdge1} onChange={e=>setinputEdge1(e.target.value)} placeholder="Edge 1"/>
              <input type='text' value={inputEdge2} onChange={e=>setinputEdge2(e.target.value)} placeholder="Edge 2"/>
              <button onClick={kekAddEdge}> add edge </button>
              <button onClick={kekClear}> clear </button>
              <button onClick={kekgetCanonicalCode}> canonical code </button>
            </div>
            {canonic_code !== '' &&
              <p>{canonic_code}</p>
            }
            {graph !== null && 
            <Graph
            key={uuidv4()}
            graph={graph}
            options={options}
            events={events}
            />}
          </TabPane>
          <TabPane tab="Получение к-деревьев из БД" key="2">
          <div className='buttons-group'>
            <input type='text' value={nvalue} onChange={e=>setnvalue(e.target.value)} placeholder="n-value"/>
            <input type='text' value={kvalue} onChange={e=>setkvalue(e.target.value)} placeholder="k-value"/>
            <label for="partial">Partial</label>
            <select id='partial' value={partial} onChange={e=>setPartial(e.target.value)} >
              <option>None</option>
              <option>Yes</option>
              <option>No</option>
            </select>
            <button onClick={kekLoadlist}> load </button>
          </div>
          {graph_list !== null && 
            <Carousel style={contentStyle}>
            {graph_list.map((g,i) => {
            return <div key={i}>
              <p style={{color:'white',fontSize:"40px"}}>{g.description}</p>
              <p style={{color:'white',fontSize:"40px"}}>{g.canonic_code} </p>
              <div>
                  <Graph
                  key={uuidv4()}
                  graph={g.graph}
                  options={options}
                  events={events}
                  />
              </div>

            </div>
          })}
             </Carousel>}      
          </TabPane>
          <TabPane tab="Статистики" key="3">
          <div>
            <h1>Time statistics</h1>
            <div id='container_time' style={{height:'500px',width:'100%'}}>

            </div>
          </div>
          
          </TabPane>
        </Tabs>
      </div>
    </div>
  );
}

export default App;
