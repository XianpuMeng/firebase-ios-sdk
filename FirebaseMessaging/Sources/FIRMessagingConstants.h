/*
 * Copyright 2017 Google
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 *  Global constants to be put here.
 *
 */
#import <Foundation/Foundation.h>

#ifndef _FIRMessaging_CONSTANTS_H
#define _FIRMessaging_CONSTANTS_H

FOUNDATION_EXPORT NSString *const kFIRMessagingRawDataKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingCollapseKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingFromKey;

FOUNDATION_EXPORT NSString *const kFIRMessagingSendTo;
FOUNDATION_EXPORT NSString *const kFIRMessagingSendTTL;
FOUNDATION_EXPORT NSString *const kFIRMessagingSendDelay;
FOUNDATION_EXPORT NSString *const kFIRMessagingSendMessageID;
FOUNDATION_EXPORT NSString *const KFIRMessagingSendMessageAppData;

FOUNDATION_EXPORT NSString *const kFIRMessagingMessageInternalReservedKeyword;
FOUNDATION_EXPORT NSString *const kFIRMessagingMessagePersistentIDKey;

FOUNDATION_EXPORT NSString *const kFIRMessagingMessageIDKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingMessageAPNSContentAvailableKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingMessageSyncViaMCSKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingMessageSyncMessageTTLKey;
FOUNDATION_EXPORT NSString *const kFIRMessagingMessageLinkKey;

FOUNDATION_EXPORT NSString *const kFIRMessagingRemoteNotificationsProxyEnabledInfoPlistKey;

FOUNDATION_EXPORT NSString *const kFIRMessagingSubDirectoryName;

// Notifications
FOUNDATION_EXPORT NSString *const kFIRMessagingCheckinFetchedNotification;
FOUNDATION_EXPORT NSString *const kFIRMessagingRegistrationTokenRefreshNotification;

FOUNDATION_EXPORT const int kFIRMessagingSendTtlDefault;  // 24 hours

/**
 *  Value included in a structured response or GCM message from IID, indicating
 *  an identity reset.
 */
FOUNDATION_EXPORT NSString *const kFIRMessaging_CMD_RST;

#pragma mark - Notifications

/// Notification used to deliver GCM messages for InstanceID.
FOUNDATION_EXPORT NSString *const kFIRMessagingCheckinFetchedNotification;
FOUNDATION_EXPORT NSString *const kFIRMessagingDefaultGCMTokenFailNotification;

FOUNDATION_EXPORT NSString *const kFIRMessagingIdentityInvalidatedNotification;

#pragma mark - Miscellaneous

/// The scope used to save the IID "*" scope token. This is used for saving the
/// IID auth token that we receive from the server. This feature was never
/// implemented on the server side.
FOUNDATION_EXPORT NSString *const kFIRMessagingAllScopeIdentifier;
/// The scope used to save the IID "*" scope token.
FOUNDATION_EXPORT NSString *const kFIRMessagingDefaultTokenScope;

/// Subdirectory in search path directory to store InstanceID preferences.
FOUNDATION_EXPORT NSString *const kFIRInstanceIDSubDirectoryName;

/// The key for APNS token in options dictionary.
FOUNDATION_EXPORT NSString *const kFIRMessagingTokenOptionsAPNSKey;

/// The key for APNS token environment type in options dictionary.
FOUNDATION_EXPORT NSString *const kFIRMessagingTokenOptionsAPNSIsSandboxKey;

/// The key for GMP AppID sent in registration requests.
FOUNDATION_EXPORT NSString *const kFIRMessagingTokenOptionsFirebaseAppIDKey;

/// The key to enable auto-register by swizzling AppDelegate's methods.
FOUNDATION_EXPORT NSString *const kFIRMessagingAppDelegateProxyEnabledInfoPlistKey;

/// Error code for missing entitlements in Keychain. iOS Keychain error
/// https://forums.developer.apple.com/thread/4743
FOUNDATION_EXPORT const int kFIRMessagingSecMissingEntitlementErrorCode;

/// The key for InstallationID or InstanceID in token request.
FOUNDATION_EXPORT NSString *const kFIRMessagingParamInstanceID;


#endif
