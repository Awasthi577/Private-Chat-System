# Decentralized Private Chat System

A censorship-resistant, end-to-end encrypted chat system designed for secure and private communication. DPCS leverages cutting-edge cryptographic protocols and decentralized networking to ensure user privacy and data integrity.

![Private Chat System UI](https://raw.githubusercontent.com/Awasthi577/Private-Chat-System/Assets/DPCS1.jpg)

## Key Technologies

  * **X3DH Key Agreement (Signal Protocol):** Establishes initial shared secrets securely.
  * **Double Ratchet:** Provides forward secrecy and post-compromise security by continuously evolving session keys.
  * **XChaCha20-Poly1305:** An authenticated encryption algorithm securing every message.
  * **libp2p GossipSub:** A peer-to-peer pub/sub messaging protocol enabling decentralized communication without central servers.


## Features

  * **End-to-End Encryption:** All messages are encrypted from sender to receiver, ensuring only the intended recipient can read them.
  * **Forward Secrecy:** Compromise of long-term keys does not compromise past messages.
  * **Deniability:** Messages cannot be definitively proven to have come from a specific sender.
  * **Decentralized Communication:** Utilizes libp2p's pub/sub mesh for robust and censorship-resistant messaging.
  * **Peer Discovery:** Kademlia DHT (Distributed Hash Table) is used for efficient peer discovery.
  * **Optional Relay for Offline Messaging:** Supports offline messaging via encrypted IPFS blobs, ensuring messages are delivered even if recipients are temporarily offline.
  * **Modern AEAD (XChaCha20-Poly1305):** Secures every message with authenticated encryption.
  * **Constant Key Rotation:** Per-message ratcheting ensures keys are constantly updated, enhancing security.
  * **Extensible Clients:** Supports various client platforms, including Web, Android, and Desktop applications.
    
   


## Architecture

The Decentralized Private Chat System is built with a layered architecture to ensure modularity, scalability, and security.

![Private Chat System UI](https://raw.githubusercontent.com/Awasthi577/Private-Chat-System/Assets/DPCS%202.jpg)

### Layers:

  * **Client Applications:** User interfaces for web, mobile, and desktop platforms. These applications are responsible for user interaction and securely managing cryptographic keys (e.g., using OS Keychain or Hardware Security Modules - HSMs).
  * **P2P Network Layer:** Handles decentralized networking using libp2p protocols. This includes Peer Discovery, Connection Management, Stream Multiplexing, and NAT Traversal.
  * **Encryption Layer:** Implements end-to-end encryption using core Signal Protocol components such as X3DH Key Exchange, Double Ratchet, and XChaCha20-Poly1305. It also manages Key Management.
  * **Storage Layer (Optional):** Provides decentralized storage and content addressing, primarily using IPFS for large media files, DHT Routing, and Content Addressing, with support for Data Replication.
  * **Transport Layer:** Facilitates message routing and pub-sub protocols, including GossipSub for efficient message delivery, Topic Management, Message Routing, and Bandwidth Control.

## Encrypted Chat Flow (Signal Protocol)

The secure communication within DPCS follows a meticulously designed flow based on the Signal Protocol.

The flow involves several key steps to ensure secure key exchange and message encryption:

1.  **Bob: Generate Key Bundle:** Bob generates an identity key, a signed prekey, and a one-time prekey.
2.  **Bob: Publish Keys:** Bob publishes his public keys to the network for discovery.
3.  **Alice: Fetch Key Bundle:** Alice retrieves Bob's public key bundle from the network.
4.  **Alice: Generate Ephemeral Key:** Alice generates an ephemeral key pair for the current session.
5.  **Alice: Perform DH Calculations:** Alice performs 4 Diffie-Hellman calculations using her own keys and Bob's keys (identity, signed prekey, one-time prekey, and Bob's ephemeral key if available).
6.  **Alice: Derive Shared Secret:** Alice combines the Diffie-Hellman outputs using HKDF to derive a shared secret.
7.  **Alice: Initialize Double Ratchet:** Alice initializes the Double Ratchet state with the derived shared secret as the root key.
8.  **Alice: Send Initial Message:** Alice encrypts and sends the first message with her ephemeral public key.

![Private Chat System Screenshot](https://raw.githubusercontent.com/Awasthi577/Private-Chat-System/Assets/DPCS%205.jpg)

![Private Chat System Screenshot](https://raw.githubusercontent.com/Awasthi577/Private-Chat-System/Assets/DPCS%206.jpg)

This process ensures that a robust shared secret is established, which then seeds the Double Ratchet for continuous key evolution and message encryption.

## Security Features

DPCS prioritizes robust security through several key features:

  * **Forward Secrecy:** Past messages remain secure even if current keys are compromised.
      * **Implementation:** Double Ratchet key deletion after use.
  * **Post-Compromise Security:** Future messages become secure again after a key compromise.
      * **Implementation:** Automatic key rotation with new DH exchanges.
  * **Metadata Protection:** Communication patterns and timing are obscured.
      * **Implementation:** Onion routing and message padding.
  * **Cryptographic Deniability:** Messages cannot be proven to come from a specific sender.
      * **Implementation:** Malleable signatures in Double Ratchet.
  * **Resistance to Attacks:** Protection against various cryptographic and network attacks.
      * **Implementation:** Constant-time operations and rate limiting.

  ![Private Chat System UI](https://raw.githubusercontent.com/Awasthi577/Private-Chat-System/Assets/DPCS%203.jpg)

## Security Checklist

To maintain the highest level of security, DPCS adheres to the following practices:

  * **AES-256 for symmetric operations:** While XChaCha20 is the default, AES-256 is also supported for strong symmetric encryption.
  * **Perfect Forward Secrecy (Double Ratchet step):** Ensures that compromise of current keys does not compromise past communications.
  * **Hardware-secure key storage:** Where possible, keys are stored in hardware-secure modules for enhanced protection.
  * **Strong authentication (MFA, rate limiting):** Implements measures like Multi-Factor Authentication and rate limiting to prevent unauthorized access and brute-force attacks.
  * **TLS 1.3 for all transport links:** Utilizes TLS 1.3 for secure communication channels in WebRTC, gRPC, and other transport layers.
  * **DDoS resistance:** Implements peer-scoring and inbound throttling to mitigate Distributed Denial of Service attacks.

## Quick Start Example (Go)

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

  * **Decentralized Discovery:** Peers locate each other using libp2p's Kademlia DHT for address lookup.
  * **Pub/Sub Messaging:** Each chat conversation operates as a mesh topic, with messages broadcast using ephemeral session keys, ensuring efficient and private group communication.
  * **End-to-End Security:** Message keys are rotated for every message, providing both forward secrecy and post-compromise security.
  * **Offline Support:** Media and files can optionally be pinned to IPFS or similar decentralized storage, referenced by Content Identifiers (CIDs) within encrypted message payloads.

## Best Practices

  * **Rotate keys daily (or on every message):** Frequent key rotation minimizes the impact of potential key compromises.
  * **Enforce constant-time cryptographic operations:** Prevents timing side-channel attacks.
  * **Pad message lengths and add jitter to timestamps (metadata protection):** Obscures communication patterns and timing to enhance privacy.
  * **Audit code and perform regular security reviews:** Continuous security assessments are crucial to identify and mitigate vulnerabilities.

## References

  * [Signal Protocol Whitepaper](https://www.google.com/search?q=https://signal.org/docs/specifications/sesamewg/sesame-latest.pdf)
  * [libp2p Specifications](https://www.google.com/search?q=https://docs.libp2p.io/concepts/overview/)
  * [XChaCha20-Poly1305 RFC](https://datatracker.ietf.org/doc/html/rfc8439)
  * [IPFS Docs](https://docs.ipfs.io/)

Clone, audit, and contribute\! Pull requests and security reviews are welcome.
