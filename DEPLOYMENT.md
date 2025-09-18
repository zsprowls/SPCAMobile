# SPCA Mobile Dashboard - Deployment Guide

## Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run app.py
   ```

3. **Access the App**
   - Open your browser to `http://localhost:8501`
   - The app is optimized for mobile devices but works on desktop too

## Mobile Testing

1. **Test on Mobile Device**
   - Find your computer's IP address
   - Access `http://YOUR_IP:8501` from your mobile device
   - Make sure both devices are on the same network

2. **Mobile-First Features**
   - Touch-friendly kennel grid
   - Swipe navigation
   - Responsive design that adapts to screen size
   - Large tap targets for easy interaction

## Data Files Required

Make sure these files are in the project directory:
- `AnimalInventory.csv` - Main animal inventory data
- `AnimalInventoryMemo.csv` - Behavior memos with adoption info

## Features

### 🏠 Dashboard Tab
- **Overview Grid**: Visual kennel layout with color-coded status
- **Drill-Down**: Tap any kennel to view detailed animal information
- **Behavior Memos**: Full behavior notes with copy functionality
- **Filtering**: Filter by location, species, and status

### 🏗️ Layout Builder Tab
- **Room Configuration**: Set grid dimensions for each location
- **Visual Editor**: Drag-and-drop kennel arrangement
- **Layout Management**: Save and load custom layouts

### 📊 Analytics Tab
- **Statistics**: Overall shelter metrics
- **Charts**: Species distribution, occupancy by location
- **Length of Stay**: Analysis of animal stay duration

## Mobile Optimization

The app is designed mobile-first with:
- Responsive grid layouts that adapt to screen size
- Touch-friendly buttons and controls
- Optimized typography for mobile reading
- Fast loading and smooth interactions

## Deployment Options

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Railway**: Deploy directly from GitHub
- **AWS/GCP**: Use container deployment

## Configuration

The app uses `.streamlit/config.toml` for configuration:
- Theme colors
- Server settings
- Browser behavior

## Troubleshooting

### Common Issues
1. **Data not loading**: Check CSV file paths and formats
2. **Layout not saving**: Ensure `layouts/` directory exists
3. **Mobile not responsive**: Clear browser cache and reload

### Performance Tips
- Use smaller CSV files for faster loading
- Enable caching for better performance
- Consider data pagination for large datasets
