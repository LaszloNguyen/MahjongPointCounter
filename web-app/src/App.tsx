import { useState } from 'react'
import styles from './App.module.scss'
import { TileSelector }from './components/TileSelector'
import { MeldedSets }from './components/MeldedSets'
import { HandTiles } from './components/HandTiles'
import { PointCalculator }from './components/PointCalculator'
import type { Tile, Meld, HandState } from './types/mahjong'

function App() {
  const [handState, setHandState] = useState<HandState>({
    handTiles: [],
    meldedSets: [],
    flowers: []
  })

  const addTileToHand = (tile: Tile) => {
    if (handState.handTiles.length < 14) {
      setHandState(prev => ({
        ...prev,
        handTiles: [...prev.handTiles, tile]
      }))
    }
  }

  const removeTileFromHand = (index: number) => {
    setHandState(prev => ({
      ...prev,
      handTiles: prev.handTiles.filter((_, i) => i !== index)
    }))
  }

  const addMeld = (meld: Meld) => {
    setHandState(prev => ({
      ...prev,
      meldedSets: [...prev.meldedSets, meld]
    }))
  }

  const removeMeld = (index: number) => {
    setHandState(prev => ({
      ...prev,
      meldedSets: prev.meldedSets.filter((_, i) => i !== index)
    }))
  }

  const addFlower = (flower: Tile) => {
    setHandState(prev => ({
      ...prev,
      flowers: [...prev.flowers, flower]
    }))
  }

  const removeFlower = (index: number) => {
    setHandState(prev => ({
      ...prev,
      flowers: prev.flowers.filter((_, i) => i !== index)
    }))
  }

  const clearHand = () => {
    setHandState({
      handTiles: [],
      meldedSets: [],
      flowers: []
    })
  }

  return (
    <div className={styles.app}>
      <header className={styles.appHeader}>
        <h1>🀄 Mahjong Point Calculator</h1>
      </header>
      
      <main className={styles.appMain}>
        <div className={styles.panelsContainer}>
          <div className={styles.panel}>
            <h2>Tile Selector</h2>
            <TileSelector 
              onTileSelect={addTileToHand}
              onFlowerSelect={addFlower}
            />
          </div>
            
          <div className={styles.panel}>
            <h2>Hand Tiles</h2>
            <HandTiles 
              tiles={handState.handTiles}
              flowers={handState.flowers}
              melds={handState.meldedSets}
              onRemoveTile={removeTileFromHand}
              onRemoveFlower={removeFlower}
              onRemoveMeld={removeMeld}
            />
          </div>
        
          <div className={styles.panel}>
            <h2>Config</h2>
            <MeldedSets 
              onAddMeld={addMeld}
              onClearHand={clearHand}
            />
          </div>
        </div>
        
        <div className={styles.calculatorPanel}>
          <PointCalculator handState={handState} />
        </div>
      </main>
    </div>
  )
}

export default App
