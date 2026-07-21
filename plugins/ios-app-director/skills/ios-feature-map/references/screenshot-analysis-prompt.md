# Screenshot Analysis Prompt

Use this prompt pattern when the user provides Stitch screenshots, exported screen images, or live Stitch screen screenshots.

The goal is to preserve the part of the manual workflow that worked well: a product/design analyst looks at the actual screens and extracts a rich feature inventory before bootstrap or implementation begins.

## Prompt Pattern

```md
I am building [APP_NAME], an iOS app for [TARGET_USER].

I created the core UI/UX experience and want you to assess the screenshots as a product designer, UX architect, and iOS app requirements analyst.

Here is what I think the app includes:
- [Feature area 1]: [short description]
- [Feature area 2]: [short description]
- [Feature area 3]: [short description]

I also created an onboarding flow:
- Welcome: [short description]
- Focus Areas: [short description]
- Set Your Goals: [short description]
- Sync Data: [short description]

The visual direction is [tone/design system summary].

I am going to provide screenshots of the app. Create a feature list from the presented layouts and map other requirements of the app based on what you see.

Please include:
1. Feature list by screen
2. Visible features
3. Functional requirements
4. Data requirements
5. AI/service/backend requirements where implied
6. Navigation structure
7. Missing or implied screens
8. Safety, privacy, consent, and claims risks
9. MVP / next release / later scope
10. Product requirement summary

Separate what is visible in the screenshots from what is inferred.
Flag anything that should not be treated as real backend behavior until implemented.
For sensitive domains, soften unsupported compliance or medical/legal/financial claims.
```

## BRAINREM Proven Example

The prompt that produced the useful BRAINREM feature plan was:

```md
I've building the AI Health Coach app and created the core UI/UX experience for you assess. Here’s what I’ve built: AI Companion: A sleek, chat-based interface where users can interact with the health coach and get insights from their data. Medications: A comprehensive tracker for logging doses, scanning barcodes, and managing daily schedules. Vitals: A dashboard for monitoring lab results, symptoms, and key health metrics like heart rate and SpO2. I've used the dark, professional aesthetic from the screenshots to ensure it feels like a high-fidelity production quality app screens. How do these look to you? Also, I've created a comprehensive onboarding flow for the AI Personal Health Coach, guiding users through four key steps: Welcome: Setting the stage for their personalized health journey. Focus Areas: Identifying the health pillars that matter most to them. Set Your Goals: Defining specific health milestones. Sync Data: Connecting their existing health data to power the AI coach's insights. The flow uses the clinical yet modern aesthetic of the Health Clinical System for a consistent and professional experience. I'm going to upload some screenshots of the app could you create a feature list from the presented layouts and map other requirements of the app based on what you see?
```

## Output Shape

Produce observations in this order before converting to section 9:

1. Screen inventory
2. Per-screen visible features
3. Per-screen implied requirements
4. Cross-screen navigation model
5. Data model clues
6. Service and AI clues
7. Risk and quality-control notes
8. Roadmap-ready feature candidates

Do not let screenshot analysis claim that a feature is implemented. A screenshot can imply a feature requirement; only code and validation prove implementation.
