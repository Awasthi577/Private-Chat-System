# Decentralized Private Chat System

A censorship-resistant, end-to-end encrypted chat system using:

- *X3DH key agreement* (Signal Protocol)
- *Double Ratchet* for forward secrecy
- *XChaCha20-Poly1305* authenticated encryption
- *libp2p GossipSub* peer-to-peer pub/sub messaging
- Decentralization (no central server)

## Features

- *End-to-end encryption* with forward secrecy and deniability
- *Decentralized communication* via libp2p pub/sub mesh
- *Peer discovery* using Kademlia DHT
- *Optional relay for offline messaging* (via encrypted IPFS blobs)
- *Modern AEAD (XChaCha20-Poly1305)* securing every message
- *Constant key rotation* (per-message ratcheting)
- *Extensible clients*: Web, Android, Desktop

## Architecture

![Architecture Diagram]

*Layers:*

- *Client*: Web/mobile/Desktop app with secure key vault (OS Keychain, HSM)
- *libp2p Node*: Multi-transport networking, Kademlia DHT, GossipSub for chat topic delivery
- *Crypto Engine*: X3DH setup, Double Ratchet, XChaCha20-Poly1305 AEAD
- *Storage (optional)*: IPFS for large media

## Signal Protocol Flow

![Signal Protocol Flow]

1. *X3DH Key Exchange:* Parties exchange keys and establish initial shared secret.
2. *Double Ratchet Initiation:* Each message exchange rotates keys for forward secrecy.
3. *XChaCha20-Poly1305 Encryption:* Ratchet keys derive symmetric keys for message encryption.
4. *Pub/Sub Messaging:* Encrypted messages relayed via GossipSub topics.

## Security Checklist

![Security Checklist]

- AES-256 for symmetric operations (use XChaCha20 as default)
- Perfect forward secrecy (Double Ratchet step)
- Hardware-secure key storage where possible
- Strong authentication (MFA, rate limiting)
- TLS 1.3 for all transport links (in WebRTC, gRPC, etc.)
- DDoS resistance: peer-score + inbound throttling

## Quick Start Example (Go)

go
// X3DH and Double Ratchet setup (using github.com/agl/ed25519/extra, github.com/libp2p/go-libp2p)
import (
    // ... imports ...
)

// 1. Key Exchange via libp2p DHT or peer-discovery
aliceBundle, bobBundle := X3DHGenerateBundles()
sharedSecret := X3DHHandshake(aliceBundle, bobBundle)

// 2. Double Ratchet state
aliceRatchet, bobRatchet := NewDoubleRatchet(sharedSecret)

// 3. Send/receive encrypted messages (via GossipSub topic)
plaintext := "Hello world!"
msg := aliceRatchet.Encrypt(plaintext)
PublishToTopic("chat_bob", msg) // pub-sub

received, err := bobRatchet.Decrypt(msg)
fmt.Println(string(received)) // "Hello world!"


## How It Works

- *Decentralized Discovery:* Peers use libp2p’s Kademlia DHT for address lookup.
- *Pub/Sub Messaging:* Each chat is a mesh topic; messages are broadcast with ephemeral session keys.
- *End-to-End Security:* Message keys rotate for every message (forward secrecy + post-compromise security).
- *Offline Support:* Media/files can optionally be pinned to IPFS or similar storage, referenced by CID in encrypted message payloads.

## Best Practices

- *Rotate keys daily (or on every message)*
- *Enforce constant-time cryptographic operations*
- *Pad message lengths and add jitter to timestamps (metadata protection)*
- *Audit code and perform regular security reviews*

## References

- Signal Protocol Whitepaper
- libp2p Specifications
- XChaCha20-Poly1305 RFC
- IPFS Docs

*Clone, audit, and contribute! Pull requests and security reviews are welcome.*
