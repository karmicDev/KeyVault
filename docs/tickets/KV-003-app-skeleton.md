# KV-003 – Flutter app skeleton (Riverpod, GoRouter)

Status: Ready
Evening: 1 · SPEC: §5 (platforms, Q13), §7

## Goal

A Flutter app in `app/` that runs on the iPhone and the Android emulator, with
routing, state management, lints and a first widget test.

## Scope

In:
- `flutter create` with org `dev.karmic` (to confirm), project name `keyvault`.
- Minimum versions: iOS 16 (`Podfile`, Xcode deployment target), Android `minSdk 30`.
- Packages: `flutter_riverpod`, `go_router`; `flutter_lints` (or stricter `very_good_analysis`, decide in plan).
- Placeholder screens and routes: `/` organisations list (empty state), `/scan`, `/request/:id`.
- Feature-first folder structure under `lib/` (described in the plan).
- One widget test: app starts and shows the empty organisations list.

Out:
- No platform channels (KV-006/007), no networking (KV-010).

## Acceptance criteria

- [ ] App launches on the physical iPhone and on the Android emulator.
- [ ] Navigating between the three placeholder routes works.
- [ ] `flutter analyze` has no issues; widget test passes.

## Check

```bash
cd app
flutter analyze
flutter test
flutter run            # once on iPhone, once on emulator (manual)
```

## Notes

- Risk: iOS code signing on the real device (~1 h). Team/bundle ID set in Xcode by the maintainer.
