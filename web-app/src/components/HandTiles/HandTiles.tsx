import type { Tile as TileType, Meld } from '../../types/mahjong'
import { Tile } from '../TileSelector';
import styles from './HandTiles.module.scss'

interface HandTilesProps {
  tiles: TileType[];
  flowers: TileType[];
  melds: Meld[];
  onRemoveTile: (index: number) => void;
  onRemoveFlower: (index: number) => void;
  onRemoveMeld: (index: number) => void;
}

const HandTiles: React.FC<HandTilesProps> = ({ tiles, flowers, melds, onRemoveTile, onRemoveFlower, onRemoveMeld }) => {
  const totalTiles = tiles.length + flowers.length
  const maxTiles = 14

  return (
    <div className={styles.handTiles}>
      <div className={styles.handSummary}>
        <h4>Hand Tiles ({tiles.length}/{maxTiles})</h4>
        {tiles.length > maxTiles && (
          <p className={styles.warning}>⚠️ Too many tiles! Remove some tiles to continue.</p>
        )}
      </div>

      <div className={styles.tilesSection}>
        <h5>Concealed Tiles ({tiles.length})</h5>
        {tiles.length === 0 && (
          <p className={styles.noMelds}>No tiles added to concealed yet.</p>
        )}
        <div className={styles.tileRow}>
          {tiles.map((tile, index) => (
            <Tile
              key={`${tile.id}-${index}`}
              className={styles.handTile}
              tile={tile}
              onClick={() => onRemoveTile(index)}
            />
          ))}
        </div>
      </div>

      <div className={styles.meldsSection}>
        <h5>Existing Melds ({melds.length})</h5>
        {melds.length === 0 ? (
          <p className={styles.noMelds}>No melds created yet.</p>
        ) : (
          <div className={styles.meldList}>
            {melds.map((meld, index) => (
              <div key={meld.id} className={styles.meldItem}>
                <div className={styles.meldInfo}>
                  <span className={styles.meldType}>
                    {meld.type.charAt(0).toUpperCase() + meld.type.slice(1)}
                  </span>
                  {meld.suit !== 'W' && meld.suit !== 'D' && (
                    <span className={styles.meldSuit}>
                      {meld.suit === 'B' ? 'Bamboo' : meld.suit === 'C' ? 'Characters' : 'Dots'} {meld.rank}
                    </span>
                  )}
                  {meld.suit === 'W' && (
                    <span className={styles.meldSuit}>
                      {meld.id === 'WE' ? 'East' : meld.id === 'WS' ? 'South' : meld.id === 'WW' ? 'West' : 'North'} Wind
                    </span>
                  )}
                  {meld.suit === 'D' && (
                    <span className={styles.meldSuit}>
                      {meld.id === 'DR' ? 'Red' : meld.id === 'DG' ? 'Green' : 'White'} Dragon
                    </span>
                  )}
                </div>
                <div className={styles.meldTiles}>
                  {meld.tiles.map((tile, tileIndex) => (
                    <span key={tileIndex} className={styles.meldTile}>
                      {tile.unicode}
                    </span>
                  ))}
                </div>
                <button
                  onClick={() => onRemoveMeld(index)}
                  className={styles.removeMeldBtn}
                  title="Remove meld"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {flowers.length > 0 && (
        <div className={styles.flowersSection}>
          <h5>Flowers & Seasons ({flowers.length})</h5>
          <div className={styles.tileRow}>
            {flowers.map((flower, index) => (
              <Tile
                key={`${flower.id}-${index}`}
                className={styles.handTile}
                tile={flower}
                onClick={() => onRemoveFlower(index)}
              />
            ))}
          </div>
        </div>
      )}

      {totalTiles === 0 && (
        <div className={styles.emptyHand}>
          <p>No tiles in hand yet.</p>
          <p>Select tiles from the Tile Selector panel to add them to your hand.</p>
        </div>
      )}

      {totalTiles > 0 && (
        <div className={styles.handStats}>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Main Tiles:</span>
            <span className={styles.statValue}>{tiles.length}</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Flowers:</span>
            <span className={styles.statValue}>{flowers.length}</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>Total:</span>
            <span className={styles.statValue}>{totalTiles}</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default HandTiles
