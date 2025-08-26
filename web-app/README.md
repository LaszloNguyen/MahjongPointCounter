# 🀄 Mahjong Point Calculator

A modern, interactive web application for calculating Mahjong hand points. Built with React, TypeScript, and Vite.

## Features

### 🎯 Three Main Panels

1. **Tile Selector Panel**
   - Complete set of Mahjong tiles (Bamboo, Characters, Dots, Winds, Dragons, Flowers & Seasons)
   - Visual tile representation with Unicode symbols
   - Easy click-to-add functionality
   - Organized by tile categories

2. **Melded Sets Panel**
   - Create and manage melded sets (Chows, Pungs, Kongs)
   - Visual tile selection interface
   - Automatic meld validation
   - Remove existing melds

3. **Hand Tiles Panel**
   - Display current hand tiles and flowers
   - Remove tiles from hand
   - Hand statistics and validation
   - Visual representation of current hand

### 🧮 Point Calculator

- **Real-time scoring** as you build your hand
- **Comprehensive point breakdown** showing how points are earned
- **Special combination detection** (All Honors, All Terminals, All One Suit)
- **Hand status validation** and feedback

### 🎨 Modern UI/UX

- **Responsive design** that works on all devices
- **Beautiful gradient backgrounds** and glass-morphism effects
- **Smooth animations** and hover effects
- **Intuitive tile management** with drag-and-drop-like functionality

## Scoring System

The calculator implements standard Mahjong scoring rules:

- **Flowers**: 1 point each
- **Pungs**: 2 points each  
- **Kongs**: 8 points each
- **Honor Tiles**: 1 point each
- **Terminal Tiles (1,9)**: 1 point each
- **Chows**: 0 points (but help form combinations)
- **Special Combinations**: Bonus points for rare hands

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- pnpm (recommended) or npm

### Installation

1. Navigate to the web-app directory:
   ```bash
   cd web-app
   ```

2. Install dependencies:
   ```bash
   pnpm install
   # or
   npm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   # or
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
pnpm build
# or
npm run build
```

## How to Use

1. **Start Building Your Hand**
   - Click on tiles in the Tile Selector panel to add them to your hand
   - Add flowers and seasons as needed

2. **Create Melded Sets**
   - Select tiles from your hand
   - Choose the meld type (Chow, Pung, or Kong)
   - Click "Create Meld" to form the set

3. **Monitor Your Points**
   - The Point Calculator panel shows real-time scoring
   - View detailed breakdown of how points are earned
   - Check hand status and validation

4. **Manage Your Hand**
   - Remove tiles you don't need
   - Clear your entire hand with the "Clear Hand" button
   - Keep track of tile counts and hand composition

## Technology Stack

- **Frontend Framework**: React 19 with TypeScript
- **Build Tool**: Vite
- **Package Manager**: pnpm
- **Styling**: CSS3 with modern features (Grid, Flexbox, CSS Variables)
- **State Management**: React Hooks (useState)
- **Type Safety**: TypeScript interfaces for all game entities

## Project Structure

```
web-app/
├── src/
│   ├── components/
│   │   ├── TileSelector.tsx      # Tile selection interface
│   │   ├── MeldedSets.tsx        # Meld creation and management
│   │   ├── HandTiles.tsx         # Hand display and management
│   │   └── PointCalculator.tsx   # Scoring calculation and display
│   ├── types/
│   │   └── mahjong.ts           # TypeScript interfaces
│   ├── App.tsx                  # Main application component
│   ├── App.css                  # Application styles
│   └── main.tsx                 # Application entry point
├── public/                      # Static assets
├── package.json                 # Dependencies and scripts
└── README.md                    # This file
```

## Contributing

This application is designed to be easily extensible. You can:

- Add new scoring rules
- Implement additional tile types
- Enhance the UI with new features
- Add multiplayer functionality
- Integrate with backend scoring engines

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Unicode Mahjong tile symbols for visual representation
- Standard Mahjong scoring rules and terminology
- Modern web development best practices and patterns
