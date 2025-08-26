import type { HandState, PointResult } from '../../types/mahjong'
import styles from './PointCalculator.module.scss'

interface PointCalculatorProps {
  handState: HandState;
}

const PointCalculator: React.FC<PointCalculatorProps> = ({ handState }) => {
  const calculatePoints = (): PointResult => {
    const { handTiles, meldedSets, flowers } = handState
    let totalPoints = 0
    const breakdown: { [key: string]: number } = {}

    // Basic flower points (1 point each)
    if (flowers.length > 0) {
      breakdown['Flowers'] = flowers.length
      totalPoints += flowers.length
    }

    // Basic meld points
    meldedSets.forEach((meld, index) => {
      if (meld.type === 'pung') {
        breakdown[`Pung ${index + 1}`] = 2
        totalPoints += 2
      } else if (meld.type === 'kong') {
        breakdown[`Kong ${index + 1}`] = 8
        totalPoints += 8
      }
      // Chows don't give points by themselves
    })

    // Honor tile points (1 point each for non-wind/non-dragon)
    const honorTiles = handTiles.filter(tile => tile.isHonor)
    if (honorTiles.length > 0) {
      breakdown['Honor Tiles'] = honorTiles.length
      totalPoints += honorTiles.length
    }

    // Terminal tile points (1 point each for 1 and 9)
    const terminalTiles = handTiles.filter(tile => 
      !tile.isHonor && !tile.isFlower && (tile.rank === 1 || tile.rank === 9)
    )
    if (terminalTiles.length > 0) {
      breakdown['Terminal Tiles'] = terminalTiles.length
      totalPoints += terminalTiles.length
    }

    // Check for special combinations
    const specialPoints = calculateSpecialCombinations(handTiles)
    Object.assign(breakdown, specialPoints.points)
    totalPoints += specialPoints.total

    return {
      totalPoints,
      breakdown,
      description: generateDescription(handState)
    }
  }

  const calculateSpecialCombinations = (handTiles: any[]) => {
    let total = 0
    const points: { [key: string]: number } = {}

    // Check for all honors hand
    const allHonors = handTiles.every(tile => tile.isHonor) && handTiles.length >= 13
    if (allHonors) {
      points['All Honors'] = 10
      total += 10
    }

    // Check for all terminals hand
    const allTerminals = handTiles.every(tile => 
      (!tile.isHonor && !tile.isFlower && (tile.rank === 1 || tile.rank === 9)) || tile.isHonor
    ) && handTiles.length >= 13
    if (allTerminals) {
      points['All Terminals'] = 10
      total += 10
    }

    // Check for all one suit
    const suits = [...new Set(handTiles.filter(t => !t.isHonor && !t.isFlower).map(t => t.suit))]
    if (suits.length === 1 && handTiles.filter(t => !t.isHonor && !t.isFlower).length >= 13) {
      points['All One Suit'] = 8
      total += 8
    }

    return { points, total }
  }

  const generateDescription = (handState: HandState): string => {
    const { handTiles } = handState
    
    if (handTiles.length === 0) {
      return 'No tiles in hand yet. Add tiles to calculate points.'
    }

    if (handTiles.length < 13) {
      return `Incomplete hand (${handTiles.length}/13 tiles). Add more tiles to complete your hand.`
    }

    if (handTiles.length === 13) {
      return 'Complete hand! You can now calculate your points.'
    }

    if (handTiles.length > 13) {
      return `Too many tiles (${handTiles.length}/13). Remove some tiles to continue.`
    }

    return 'Hand status unknown.'
  }

  const result = calculatePoints()

  return (
    <div className={styles.pointCalculator}>
      <h3>Point Calculator</h3>
      
      <div className={styles.calculationResult}>
        <div className={styles.totalPoints}>
          <span className={styles.pointsLabel}>Total Points</span>
          <span className={styles.pointsValue}>{result.totalPoints}</span>
        </div>

        {Object.keys(result.breakdown).length > 0 ? (
          <div className={styles.pointsBreakdown}>
            <h4>Points Breakdown</h4>
            <ul className={styles.breakdownList}>
              {Object.entries(result.breakdown).map(([label, points]) => (
                <li key={label} className={styles.breakdownItem}>
                  <span className={styles.breakdownLabel}>{label}</span>
                  <span className={styles.breakdownValue}>{points}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <p className={styles.noPoints}>No points calculated yet.</p>
        )}
      </div>

      <div className={styles.handStatus}>
        <h4>Hand Status</h4>
        <p className={styles.statusDescription}>{result.description}</p>
        
        <div className={styles.handSummary}>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Hand Tiles</span>
            <span className={styles.summaryValue}>{handState.handTiles.length}</span>
          </div>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Melded Sets</span>
            <span className={styles.summaryValue}>{handState.meldedSets.length}</span>
          </div>
          <div className={styles.summaryItem}>
            <span className={styles.summaryLabel}>Flowers</span>
            <span className={styles.summaryValue}>{handState.flowers.length}</span>
          </div>
        </div>
      </div>

      <div className={styles.scoringInfo}>
        <h4>Scoring Information</h4>
        <ul className={styles.scoringList}>
          <li>Flowers: 1 point each</li>
          <li>Pungs: 2 points each</li>
          <li>Kongs: 8 points each</li>
          <li>Honor tiles: 1 point each</li>
          <li>Terminal tiles (1, 9): 1 point each</li>
          <li>All honors hand: 10 bonus points</li>
          <li>All terminals hand: 10 bonus points</li>
          <li>All one suit: 8 bonus points</li>
        </ul>
      </div>
    </div>
  )
}

export default PointCalculator
