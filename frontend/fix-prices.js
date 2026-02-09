// frontend/fix-prices.js - Quick fix for price consistency
// Run this in browser console if needed

(function() {
    console.log('🔧 Fixing price consistency...');
    
    // Update the quick estimate calculation to match full prediction
    window.HousePriceAI.calculateQuickEstimate = function(values) {
        const basePrice = 200000;
        const roomValue = values.totalRooms * 18000;
        const bedroomValue = values.bedrooms * 22000;
        const ageAdjustment = values.houseAge * -1200;
        const incomeFactor = values.income * 1500;
        const populationFactor = Math.min(values.population / 100, 50) * 100;
        const householdFactor = Math.min(values.households / 50, 40) * 100;
        
        const oceanPremium = {
            1: 30000,
            2: 50000,
            3: 0,
            4: 80000
        }[values.oceanProximity] || 0;
        
        const price = basePrice + roomValue + bedroomValue + ageAdjustment + 
                     incomeFactor + populationFactor + householdFactor + oceanPremium;
        
        return Math.round(Math.max(price, 150000) / 1000) * 1000;
    };
    
    console.log('✅ Price calculations now consistent!');
    console.log('🔄 Refreshing quick estimate...');
    
    // Refresh the display
    if (typeof window.HousePriceAI.updateQuickEstimate === 'function') {
        window.HousePriceAI.updateQuickEstimate();
    }
})();