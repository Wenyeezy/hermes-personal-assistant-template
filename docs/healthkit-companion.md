# HealthKit Companion Distribution

Hermes supports a separately installed iPhone companion that reads only the
HealthKit types its owner approves and sends a summarized daily payload to the
fork owner's authenticated Hermes ingest endpoint.

## Recommended Friend Path: TestFlight

The maintainer may invite a friend as an external TestFlight tester. This shares
an installable beta build—not the Apple Developer password, signing certificate,
provisioning profile, App Store Connect role, or any existing user's Health data.

Apple's supported flow is: create an external testing group, attach an approved
build, and invite the tester by email. External testing may require Beta App
Review. See [Apple's TestFlight external tester guide](https://developer.apple.com/help/app-store-connect/test-a-beta-version/invite-external-testers).

After installation, the friend should configure their own endpoint and unique
username/password in the app. Do not prefill the maintainer's production domain
or credentials.

## Fork Owner Ingest Setup

On the Mac running Hermes:

```text
export HERMES_HEALTH_USERNAME="hermes"
export HERMES_HEALTH_PASSWORD="a-long-unique-password"
python3 scripts/hermes.py health-ingest --host 0.0.0.0 --port 9121
```

The iPhone endpoint on the same private network is:

```text
http://MAC_LAN_IP:9121/health/import
```

The ingest service exposes only health import/status, authentication check, and
confirmed Nutrition export. It refuses to start without a password. The main
Dashboard remains loopback-only. For access outside a trusted LAN, use an
authenticated HTTPS tunnel and do not expose port 9121 directly to the internet.

## Build-Your-Own Path

The portable contract is documented by these endpoints:

- `GET /healthz` — unauthenticated reachability only;
- `GET /health/authz` — Basic-auth credential check;
- `POST /health/import` — daily summary plus workouts;
- `GET /health/status?date=YYYY-MM-DD` — import confirmation;
- `GET /nutrition/export?date=YYYY-MM-DD` — confirmed nutrients for optional
  HealthKit write-back.

A separately maintained sample iOS source project can use its own Bundle ID,
Apple team, and HealthKit entitlement. Apple requires the HealthKit capability,
purpose strings, and fine-grained owner authorization for each read/write type;
see [Authorizing access to health data](https://developer.apple.com/documentation/HealthKit/authorizing-access-to-health-data).

## Payload Contract

```json
{
  "source": "apple_health_bridge",
  "recorded_at": "2026-08-11T09:30:00Z",
  "daily": {
    "date": "2026-08-11",
    "steps": 9876,
    "exercise_min": 42,
    "standing_minutes": 610,
    "active_calories": 530,
    "resting_calories": 1760,
    "distance_km": 7.4
  },
  "workouts": [
    {
      "activity": "walking",
      "event_time": "2026-08-11T08:10:00Z",
      "duration_min": 35,
      "active_calories": 210,
      "distance": 3.2,
      "source_id": "device-generated-stable-id"
    }
  ]
}
```

Keep raw Health exports, endpoint passwords, device identifiers, signing assets,
and real payload samples outside the public repository.
