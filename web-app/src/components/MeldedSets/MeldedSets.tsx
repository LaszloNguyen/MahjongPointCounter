import { useState } from 'react'
import type { Meld, Tile } from '../../types/mahjong'
import styles from './MeldedSets.module.scss'

interface MeldedSetsProps {
  onAddMeld: (meld: Meld) => void;
  onClearHand: () => void;
}

const MeldedSets: React.FC<MeldedSetsProps> = ({ onAddMeld, onClearHand }) => {
  const [selectedTiles, setSelectedTiles] = useState<Tile[]>([])
  const [meldType, setMeldType] = useState<'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2'>('pung2')

  // This function is for future use when implementing drag-and-drop functionality
  // const addTileToSelection = (tile: Tile) => {
  //   if (selectedTiles.length < 4) {
  //     setSelectedTiles([...selectedTiles, tile])
  //   }
  // }

  const removeTileFromSelection = (index: number) => {
    setSelectedTiles(selectedTiles.filter((_, i) => i !== index))
  }

  const createMeld = () => {
    if (selectedTiles.length < 3 || selectedTiles.length > 4) return

    // Validate meld
    const isValidMeld = validateMeld(selectedTiles, meldType)
    if (!isValidMeld) {
      alert('Invalid meld! Please check your tile selection.')
      return
    }

    const meld: Meld = {
      id: `meld-${Date.now()}`,
      type: meldType,
      tiles: [...selectedTiles],
      suit: selectedTiles[0].suit,
      rank: selectedTiles[0].rank
    }

    onAddMeld(meld)
    setSelectedTiles([])
  }

  const validateMeld = (tiles: Tile[], type: string): boolean => {
    if (type === 'chow' || type === 'chow2') {
      // Chow: 3 consecutive tiles of same suit
      if (tiles.length !== 3) return false
      if (tiles.some(t => t.isHonor || t.isFlower)) return false
      if (tiles.some(t => t.suit !== tiles[0].suit)) return false
      
      const ranks = tiles.map(t => t.rank!).sort((a, b) => a - b)
      return ranks[1] === ranks[0] + 1 && ranks[2] === ranks[1] + 1
    } else if (type === 'pung' || type === 'pung2') {
      // Pung: 3 identical tiles
      if (tiles.length !== 3) return false
      return tiles.every(t => t.id === tiles[0].id)
    } else if (type === 'kong' || type === 'kong2') {
      // Kong: 4 identical tiles
      if (tiles.length !== 4) return false
      return tiles.every(t => t.id === tiles[0].id)
    }
    return false
  }

  const clearSelection = () => {
    setSelectedTiles([])
  }

  return (
    <div className={styles.meldedSets}>
      <div className={styles.meldCreator}>
        <h4>Add to hand method</h4>
        <div className={styles.meldTypeSelector}>
          <div className={styles.column}>
            <label>
              <input
                type="radio"
                name="meldType"
                value="chow"
                checked={meldType === 'chow'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Chow (3 consecutive)
            </label>
            <label>
              <input
                type="radio"
                name="meldType"
                value="pung"
                checked={meldType === 'pung'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Pung (3 identical)
            </label>
            <label>
              <input
                type="radio"
                name="meldType"
                value="kong"
                checked={meldType === 'kong'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Melded Kong (4 identical)
            </label>
          </div>
          <div className={styles.column}>
            <label>
              <input
                type="radio"
                name="meldType"
                value="chow2"
                checked={meldType === 'chow2'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Concerned Kong
            </label>
            <label>
              <input
                type="radio"
                name="meldType"
                value="pung2"
                checked={meldType === 'pung2'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Concealed Tile
            </label>
            <label>
              <input
                type="radio"
                name="meldType"
                value="kong2"
                checked={meldType === 'kong2'}
                onChange={(e) => setMeldType(e.target.value as 'chow' | 'pung' | 'kong' | 'chow2' | 'pung2' | 'kong2')}
              />
              Winning Tile
            </label>
          </div>
        </div>

        <div className={styles.selectedTiles}>
          <h5>Selected Tiles ({selectedTiles.length})</h5>
          <div className={styles.tileSelection}>
            {selectedTiles.map((tile, index) => (
              <div key={index} className={styles.selectedTile}>
                <span>{tile.unicode}</span>
                <button
                  onClick={() => removeTileFromSelection(index)}
                  className={styles.removeTileBtn}
                  title="Remove tile"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.meldActions}>
          <button
            onClick={createMeld}
            className={styles.createMeldBtn}
            disabled={selectedTiles.length < 3 || selectedTiles.length > 4}
          >
            Create Meld
          </button>
          <button
            onClick={clearSelection}
            className={styles.clearSelectionBtn}
          >
            Clear Selection
          </button>
        </div>
      </div>
      
      <button onClick={onClearHand} className={styles.clearButton}>
        Clear Hand
      </button>
    </div>
  )
}

export default MeldedSets
