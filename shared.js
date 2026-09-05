import { createStore } from 'https://esm.sh/zustand/vanilla';
import { persist } from 'https://esm.sh/zustand/middleware';

export const useGamificationStore = createStore(
  persist(
    (set, get) => ({
      xp: 0,
      streak: { current: 0, lastActiveDate: '' },
      completedTopics: [],
      sm2Data: {}, // questionId -> { interval, repetition, easinessFactor, nextReview }

      addXP: (amount) => set((state) => {
        const newXp = state.xp + amount;
        updateHud(newXp, state.streak.current);
        return { xp: newXp };
      }),

      updateSM2: (id, data) => set((state) => ({
        sm2Data: { ...state.sm2Data, [id]: data }
      })),
      
      checkStreak: () => set((state) => {
        const today = new Date().toISOString().split('T')[0];
        if (state.streak.lastActiveDate === today) return state;
        
        let newStreak = state.streak.current;
        const lastDate = new Date(state.streak.lastActiveDate);
        const current = new Date(today);
        const diffDays = Math.floor((current - lastDate) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
          newStreak += 1;
        } else if (diffDays > 1) {
          newStreak = 1;
        } else {
          newStreak = 1; // first time
        }
        
        updateHud(state.xp, newStreak);
        return { streak: { current: newStreak, lastActiveDate: today } };
      })
    }),
    {
      name: 'tarangam-gamification-storage',
    }
  )
);

// SM-2 Algorithm implementation
export function sm2Advance(previousData, quality) {
  let { interval = 0, repetition = 0, easinessFactor = 2.5 } = previousData || {};
  
  if (quality >= 3) {
    if (repetition === 0) {
      interval = 1;
    } else if (repetition === 1) {
      interval = 6;
    } else {
      interval = Math.round(interval * easinessFactor);
    }
    repetition += 1;
  } else {
    repetition = 0;
    interval = 1;
  }
  
  easinessFactor = easinessFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  if (easinessFactor < 1.3) easinessFactor = 1.3;
  
  // Next review date
  const now = new Date();
  now.setDate(now.getDate() + interval);
  
  return { interval, repetition, easinessFactor, nextReview: now.getTime() };
}

// Initial HUD render
function updateHud(xp, streak) {
  const hud = document.getElementById('gamification-hud');
  if (hud) {
    hud.innerHTML = `
      <div style="display: flex; gap: 1rem; align-items: center; font-weight: 600;">
        <span style="color: #fbbf24; background: rgba(251,191,36,0.1); padding: 0.25rem 0.5rem; border-radius: 6px;">🔥 ${streak} Day Streak</span>
        <span style="color: #60a5fa; background: rgba(96,165,250,0.1); padding: 0.25rem 0.5rem; border-radius: 6px;">✨ ${xp} XP</span>
        <a href="/review.html" style="color: var(--accent); border: 1px solid var(--accent); padding: 0.25rem 0.5rem; border-radius: 6px; text-decoration: none;">Review Deck</a>
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  useGamificationStore.getState().checkStreak();
  updateHud(useGamificationStore.getState().xp, useGamificationStore.getState().streak.current);
});
window.useGamificationStore = useGamificationStore;
window.sm2Advance = sm2Advance;
